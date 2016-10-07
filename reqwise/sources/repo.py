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
import yum

LOG = logging.getLogger('__main__')


class Yum(object):
    """Represents the local defined repositories."""

    def __init__(self, repos='all', disabled=False, fields=['name']):
        self.name = 'yum'
        self.repos = repos
        self.yum = yum.YumBase()
        self.repos = (self.yum).repos.listEnabled()
        self.ready = self.setup()
        self.disabled = disabled
        self.fields = fields

    def setup(self):
        """Returns bool to indicate whether the source is ready

           or not.
        """
        return len(self.repos)

    def search(self, req):
        """Search for requirement with yum.

        Returns {'found': True/False }
        """
        LOG.debug("Looking for %s", req.name)

        result = (self.yum).searchGenerator(self.fields, [req.name])
        for (package, matched_value) in result:
            LOG.info(package)
