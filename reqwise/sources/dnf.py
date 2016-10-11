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
import re
import yum

import common.utils as utils
from result import Result
from source import Source

LOG = logging.getLogger('__main__')


class Yum(Source):
    """Represents the local defined repositories."""

    def __init__(self, repos='all', disabled=False, fields=['name']):
        super(Yum, self).__init__('yum', disabled)
        self.repos = repos
        self.yum = yum.YumBase()
        self.repos = (self.yum).repos.listEnabled()
        self.ready = self.setup()
        self.fields = fields

    def setup(self):
        """Returns bool to indicate whether the source is ready

           or not.
        """
        return len(self.repos)

    def search(self, req, long_ver=False):
        """Returns list of Result object based on the RPMs it found that

        match the requirement name.
        """
        found_pkgs = []

        match = (self.yum).searchGenerator(self.fields, [req.name])
        for (rpm, rpm_name) in match:
            name = (re.search(r'(^[a-zA-z0-9\-]*)\-\d', str(rpm))).group(1)
            if utils.verify_name(name, req.name):
                name, version, os, arch = utils.get_rpm_details(
                    str(rpm), long_ver)
                found_pkgs.append(Result(name, version, self.name, os, arch))

        return found_pkgs
