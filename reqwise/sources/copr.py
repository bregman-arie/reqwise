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
import requests

LOG = logging.getLogger('__main__')


class Copr(object):
    """Represents Fedora COPR"""

    def __init__(self, project, disabled=True):
        self.name = 'copr'
        self.ready = self.setup()
        self.projects = projects
        self.disabled = False if self.repos else True

    def setup(self):
        """Returns bool to indicate whether the source is ready

           or not.
        """
        response = requests.get("http://copr.fedoraproject.org")
        return response.status_code

    def search(self, req):
        """Returns list of Result object based on the RPMs it found that

        match the requirement name.
        """
        projects = requests.get...
