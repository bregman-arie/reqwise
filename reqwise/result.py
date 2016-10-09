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
from termcolor import colored

LOG = logging.getLogger(__name__)


class Result(object):

    def __init__(self, rpm_name, version, os, arch, source):
        self.rpm_name = rpm_name
        self.version = version
        self.os = os
        self.arch = arch
        self.source = source

    def __str__(self):
        result_output = []
        result_output.append("Found {} {} {} {} in source: {}".format(
            colored(self.rpm_name, 'green'), colored(self.version, 'cyan'),
            self.os, self.arch, colored(self.source, 'magenta')))
        return '\n'.join(result_output)

    @staticmethod
    def report(results):
        """Logging all results with all the collected data."""

        for req, results in results.items():
            if len(results):
                LOG.info("\n== %s ==\n", colored(req, 'green'))
            else:
                LOG.info("\n== %s ==\n", colored(req, 'red'))
            for result in results:
                LOG.info(result)
