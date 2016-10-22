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
import dnf
import logging

import common.utils as utils
from result import Result
from source import Source

LOG = logging.getLogger('__main__')


class Dnf(Source):
    """Represents the local defined repositories."""

    def __init__(self, repos='all', disabled=False, fields=['name']):
        super(Dnf, self).__init__('dnf', disabled)
        self.repos = repos
        self.base = dnf.Base()
        self.ready = self.setup()
        self.fields = fields

    def setup(self):
        """Returns bool to indicate whether the source is ready

           or not.
        """
        (self.base).read_all_repos()
        (self.base).fill_sack()
        return len(self.base.repos)

    def search(self, req, long_ver=False):
        """Returns list of Result object based on the RPMs it found that

        match the requirement name.
        """
        found_pkgs = []
        query = self.base.sack.query()
        rpms = query.available()
        rpms = rpms.filter(name__substr=req.name)

        for rpm in rpms:
            if (utils.verify_name(rpm.name, req.name) and
               req.meet_the_specs(rpm.version)):
                found_pkgs.append(Result(rpm.name, rpm.version, self.name,
                                         rpm.release, rpm.arch,
                                         rpm.reponame))

        return found_pkgs
