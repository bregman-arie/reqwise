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
from sources.repo import Yum
import utils

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
LOG = logging.getLogger(__name__)


class Manager(object):
    """Represents the program manager.

       Reads config file if present.
       Sets all the available sources.
       Reads the requirements.
       Search for requirements in the different sources.
    """
    def __init__(self, path=None, conf=None):
        self.path = path or os.getcwd()
        self.config = conf or self.get_config()
        self.req_files = utils.find_req_files(self.path)
        self.requirements = self.get_requirements()
        self.sources = self.get_sources()

    def get_requirements(self):
        """Returns list of requirement objects."""
        requirements = []
        for req_file in self.req_files:
            with open(req_file, 'r') as req_f:
                for req in req_f:
                    requirements.append(Requirement(req.strip()))

        return requirements

    def get_sources(self):
        """Returns list of sources."""
        if self.config:
            return []
        else:
            return [Yum()]
        
    def get_config(self):
        """Returns config file path."""
        if os.path.isfile(os.getcwd() + '/reqwise.conf'):
            return os.getcwd() + '/reqwise.conf'
        else:
            return os.path.isfile('/etc/reqwise/reqwise.conf')

    def anaylze(self):
        """Search for requirements in the different sources."""

        result = []
        for source in self.sources:
            if source.ready:
                LOG.info("Source: {}".format(source.name))
                for req in self.requirements:
                    result.append(source.search(req))
            else:
                LOG.debug("Source: %s is disabled", source.name)
