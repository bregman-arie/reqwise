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
import logging
import os

from requirement import Requirement
from result import Result
from sources.copr import Copr
from sources.dnf import Yum
import utils

LOG = logging.getLogger('__main__')


class Manager(object):
    """Represents the program manager.

       Reads config file if present.
       Sets all the available sources.
       Reads the requirements.
       Search for requirements in the different sources.
    """
    def __init__(self, args):
        self.results = {}
        self.path = args.path or os.getcwd()
        self.config = self.get_config()
        self.req_files = utils.find_req_files(self.path)
        self.requirements = self.get_requirements()
        self.copr_projects = args.copr_projects or None
        self.sources = self.get_sources()

    def get_requirements(self):
        """Returns list of requirement objects."""
        requirements = []
        for req_file in self.req_files:
            with open(req_file, 'r') as req_f:
                for req in req_f:
                    requirements.append(Requirement(req.strip()))
                    self.results[requirements[-1].name] = []

        return requirements

    def get_sources(self):
        """Returns list of sources."""
        if self.config:
            return []
        else:
            return [Yum(), Copr(self.copr_projects)]

    def get_config(self):
        """Returns config file path."""
        if os.path.isfile(os.getcwd() + '/reqwise.conf'):
            return os.getcwd() + '/reqwise.conf'
        else:
            return os.path.isfile('/etc/reqwise/reqwise.conf')

    def start(self):
        """Start searching for all the requirements in all the sources."""

        for req in self.requirements:
            for source in self.sources:
                if source.ready and not source.disabled:
                    LOG.debug("Looking in source: %s", source.name)
                    source_results = source.search(req)
                    (self.results[req.name]).extend(source_results)
                else:
                    LOG.debug("Source: %s is disabled", source.name)

        Result.report(self.results)
