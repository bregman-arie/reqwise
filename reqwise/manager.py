# Copyright 2016 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import glob
import logging
import os
from pkg_resources import Requirement as Req
from termcolor import colored

import requirement
from result import Result
from sources.copr import Copr
from sources.yum import Dnf
from sources.koji import Koji

LOG = logging.getLogger(__name__)


class Manager(object):
    """Represents the program manager.

       Reads config file if present.
       Sets all the available sources.
       Reads the requirements.
       Search for requirements in the different sources.
    """

    def __init__(self, args):
        self.results = {}
        self.config = self.get_config()
        self.reqs = args.reqs or None
        self.req_files = self.find_req_files(self.reqs)
        self.requirements = self.get_requirements()
        self.copr_projects = args.copr_projects or None
        self.sources = self.get_sources()
        self.long = args.long or None
        self.missingOnly = args.missing or False

    def get_requirements(self):
        """Returns list of requirement objects."""
        requirements = []
        for req_file in self.req_files:
            with open(req_file, 'r') as req_f:
                for line in req_f:
                    if not line.startswith('#'):
                        parsed_req = Req.parse(line.strip())
                        requirements.append(requirement.Requirement(
                            parsed_req.unsafe_name, parsed_req.specs))
                        self.results[requirements[-1].name] = []

        return requirements

    def get_sources(self):
        """Returns list of sources."""
        if self.config:
            return []
        else:
            return [Dnf(), Copr(self.copr_projects), Koji()]

    def get_config(self):
        """Returns config file path."""
        if os.path.isfile(os.getcwd() + '/reqwise.conf'):
            return os.getcwd() + '/reqwise.conf'
        else:
            return os.path.isfile('/etc/reqwise/reqwise.conf')

    @staticmethod
    def find_req_files(reqs):
        """Returns list of absolute paths of the requirement files."""
        if not reqs:
            if glob.glob(os.getcwd() + '/*requirements*'):
                return glob.glob(os.getcwd() + '/*requirements*')
            else:
                raise Exception("Couldn't find any requirement files.\
 Please provide path or files")
        elif os.path.isfile(reqs):
            return [reqs]
        elif glob.glob(reqs + '/*requirements*'):
            return glob.glob(reqs + '/*requirements*')
        else:
            raise Exception("Couldn't find any requirements...\
 tried {}".format(reqs))

    def start(self):
        """Start searching for all the requirements in all the sources."""

        LOG.info("Looking for requirement files")
        self.req_files = self.find_req_files(self.reqs)
        one_source_active = False
        LOG.info("Querying for RPMs")

        for req in self.requirements:
            for source in self.sources:
                if source.ready and not source.disabled:
                    one_source_active = True
                    LOG.debug("Looking in source: %s", source.name)
                    source_results = source.search(req, self.long)
                    (self.results[req.name]).extend(source_results)
            self.results[req.name] = set(self.results[req.name])

        if one_source_active:
            Result.report(self.results, self.missingOnly)
        else:
            LOG.error(colored(
                "Couldn't use any source. Check your connectivity...", 'red'))
