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
from distutils.version import StrictVersion
import operator as py_operator


class Requirement(object):

    def __init__(self, name, specs):
        self.name = name
        self.specs = specs

    def meet_the_specs(self, version):
        """Returns True if the given version meets the specs of the Requirement

           instance.
        """

        op_map = {
                    '==': 'eq', '=':  'eq', 'eq': 'eq',
                    '<':  'lt', 'lt': 'lt',
                    '<=': 'le', 'le': 'le',
                    '>':  'gt', 'gt': 'gt',
                    '>=': 'ge', 'ge': 'ge',
                    '!=': 'ne', '<>': 'ne', 'ne': 'ne'
                }

        for spec in self.specs:
            operator = op_map[spec[0]]
            cmp_method = getattr(py_operator, operator)

            if not cmp_method(StrictVersion(str(version)),
                              StrictVersion(str(spec[1]))):
                return False
        return True
