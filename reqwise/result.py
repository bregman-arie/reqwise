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

HEADERS = ["Name", "Version", "Source", "Repository"]
SPACES = 25


class Result(object):

    def __init__(self, name, version, source, os=None, arch=None,
                 repo=''):
        self.name = name
        self.version = version
        self.os = os
        self.arch = arch
        self.source = source
        self.repo = repo

    @staticmethod
    def report(all_results, missingOnly):
        """Logging all results with all the collected data."""

        for name, results in all_results.items():
            if results:
                if not missingOnly:
                    LOG.info("\n" + "="*SPACES + " " + colored(
                        name, 'green') + " " + "="*SPACES)
                    req_table = []
                    for result in results:
                        req_table.append([colored(result.name, 'green'),
                                          colored(result.version, 'cyan'),
                                          colored(result.source, 'magenta'),
                                          colored(result.repo, 'magenta')])

                    LOG.info(tabulate(req_table, HEADERS, tablefmt="fancy_grid"))
            else:
                LOG.info("\n" + "="*SPACES + " " + colored(
                    name, 'red') + " " + "="*16)
                LOG.info("\n" + " "*SPACES + colored(
                    "Not Found", 'red') + " "*SPACES)

    def __eq__(self, other):
        return (self.name == other.name and self.version == other.version and
                self.source == other.source)

    def __hash__(self):
        return hash(('name', self.name, 'version', self.version,
                     'source', self.source))
