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

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

class Yum(object):
    """Represents the local defined repositories."""

    def __init__(self, repos='all'):
        self.name = 'yum'
        self.repos = repos
        self.yum = yum.YumBase()
        self.repos = (self.yum).repos.listEnabled()

    def find(self, req):
        """Search for requirement with yum."""
        if not len(self.repos):
            logger.info("No repos enabled. Skipping yum check...")
        else:
            logger.info("Looking for {}".format(req.name))
