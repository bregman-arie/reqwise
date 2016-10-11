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
from urlparse import urljoin
from urlparse import urlparse

import logging
import requests

import common.utils as utils
from result import Result

LOG = logging.getLogger('__main__')


class Copr(object):
    """Represents Fedora COPR"""

    def __init__(self, projects, disabled=True):
        self.name = 'copr'
        self.copr = urlparse("https://copr.fedorainfracloud.org")
        self.projects = projects
        self.ready = self.setup()
        self.disabled = False if self.projects else True

    def setup(self):
        """Returns bool to indicate whether the source is ready

           or not.
        """
        response = requests.get(self.copr.geturl())
        return response.status_code

    def get_project_id(self, name):
        """Returns COPR project id based on the name."""
        project_data_url = urljoin(self.copr.geturl(),
                                   '/api_2/projects?name=' + self.projects)
        project_data = (requests.get(project_data_url)).json()

        return project_data['projects'][0]['project']['id']

    def get_built_packages(self, id):
        """Returns built packages based1 on the provided ID."""
        built_pkgs_url = urljoin(self.copr.geturl(),
                                 '/api_2/builds?project_id=' + str(id))
        built_pkgs = (requests.get(built_pkgs_url)).json()

        return built_pkgs['builds']

    def search(self, req):
        """Returns list of Result object based on the RPMs it found that

           match the requirement name.
        """
        found_pkgs = []
        project_id = self.get_project_id(self.projects)
        built_pkgs = self.get_built_packages(project_id)

        for pkg in built_pkgs:
            version = pkg['build']['built_packages'][0]['version']
            name = pkg['build']['built_packages'][0]['name']
            if utils.verify_name(str(name), req.name):
                found_pkgs.append(Result(name, version, self.name))

        return found_pkgs
