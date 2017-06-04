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
from pkg_resources import Requirement as Req

from reqwise.requirement import Requirement
from reqwise.result import Result
from reqwise.sources.copr import Copr
from reqwise.sources.yum import Dnf
from reqwise.sources.koji import Koji

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
        self.req_files = Requirement.find_req_files(self.reqs)
        self.requirements = self.get_requirements()
        self.copr_projects = args.copr_projects or None
        self.koji = args.koji or False
        self.sources = self.get_sources()
        self.long = args.long or None
        self.missing_only = args.missing or False
        self.convert_only = args.convert or False

    def get_requirements(self):
        """Returns list of requirement objects."""
        requirements = []
        LOG.debug("Reading requirements")

        for req_file in self.req_files:
            with open(req_file, 'r') as req_f:
                for line in req_f:
                    if not line.startswith('#'):
                        parsed_req = Req.parse(line.strip())
                        requirements.append(Requirement(
                            parsed_req.unsafe_name, parsed_req.specs))
                        self.results[requirements[-1].name] = []

        return requirements

    def get_sources(self):
        """Returns list of sources to use."""
        LOG.info("Generating list of active sources")
        sources = [Dnf()]
        if self.koji:
            sources.append(Koji())
        if self.copr_projects:
            sources.append(Copr(self.copr_projects))

        return sources

    def get_config(self):
        """Returns config file path."""
        if os.path.isfile(os.getcwd() + '/reqwise.conf'):
            return os.getcwd() + '/reqwise.conf'
        else:
            return os.path.isfile('/etc/reqwise/reqwise.conf')

    def convert_and_search(self):
        """Convert pip packages list to RPMs and search for them in them

        different sources.
        """
        LOG.info("Querying for RPMs")
        for req in self.requirements:
            for source in self.sources:
                if source.ready and not source.disabled:
                    LOG.debug("Looking for %s in source: %s" % (req.name,
                                                                source.name,))
                    source_results = source.search_all(req, self.long)
                    (self.results[req.name]).extend(source_results)
            self.results[req.name] = set(self.results[req.name])

        Result.report(self.results, self.missing_only)

    def convert(self):
        """Convert pip packages list to RPMs based on first search result"""
        rpms = []
        for req in self.requirements:
            for source in self.sources:
                if source.ready and not source.disabled:
                    rpm = source.search_one(req)
                    if rpm:
                        rpms.append(rpm)
                        break
        LOG.info('\n'.join(set(rpms)))

    def start(self):
        """Start the run of reqwise."""

        if not self.convert_only:
            LOG.debug("Converting pip packages list to RPM(s) and searching \
for the RPM(s) in the different sources.")
            self.convert_and_search()
        else:
            LOG.debug("Converting pip packages list to RPM(s)")
            self.convert()
