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
import utils

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


class Manager(object):

    def __init__(self, path=None):
        self.path = path or os.getcwd()
        self.req_files = utils.find_req_files(self.path)

    def get_requirements(self):
        """Returns list of requirement objects."""
        requirements = []
        for req_file in self.req_files:
            with open(req_file, 'r') as req_f:
                for req in req_f:
                    requirements.append(Requirement(req.strip()))

        return requirements
