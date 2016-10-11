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
import subprocess
from urlparse import urlparse

import logging
import requests

import common.utils as utils
from result import Result
from source import Source

LOG = logging.getLogger('__main__')


class Koji(Source):
    """Represents Fedora Koji build system"""

    def __init__(self, disabled=False):
        super(Koji, self).__init__('koji', disabled)
        self.url = urlparse('http://koji.fedoraproject.org')
        self.cmd = 'koji search rpm -r '
        self.ready = self.setup()

    def setup(self):
        """Returns bool to indicate whether the source is ready

           or not.
        """
        response = requests.get(self.url.geturl())
        cmd_exists = utils.cmd_exists(self.name)

        return (response.status_code and cmd_exists)

    def search(self, req, long_ver=False):
        """Returns list of Result object based on the RPMs it found that

           match the requirement name.
        """
        found_pkgs = []
        rpms = subprocess.Popen(self.cmd + req.name, shell=True,
                                stdout=subprocess.PIPE).stdout.read()

        for rpm in rpms.split():
            name, version, os, arch = utils.get_rpm_details(rpm, long_ver)
            if ".src." not in rpm and utils.verify_name(name, req.name):
                found_pkgs.append(Result(name, version, self.name, os, arch))

        return found_pkgs
