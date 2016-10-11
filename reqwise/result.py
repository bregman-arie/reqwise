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
from tabulate import tabulate
from termcolor import colored

LOG = logging.getLogger(__name__)

HEADERS = ["Name", "Version", "Source"]


class Result(object):

    def __init__(self, rpm_name, version, source, os=None, arch=None):
        self.rpm_name = rpm_name
        self.version = version
        self.os = os
        self.arch = arch
        self.source = source

    @staticmethod
    def report(all_results):
        """Logging all results with all the collected data."""

        for name, results in all_results.items():
            if results:
                LOG.info("\n" + "="*16 + " " + colored(
                    name, 'green') + " " + "="*16)
                req_table = []
                for result in results:
                    req_table.append([colored(result.rpm_name, 'green'),
                                      colored(result.version, 'cyan'),
                                      colored(result.source, 'magenta')])

                LOG.info(tabulate(req_table, HEADERS, tablefmt="fancy_grid"))
            else:
                LOG.info("\n" + "="*16 + " " + colored(
                    name, 'red') + " " + "="*16)
                LOG.info("\n" + " "*16 + colored("Not Found", 'red') + " "*16)
