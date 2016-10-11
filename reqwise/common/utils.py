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
import re

import common.constants as const


def verify_name(self, match, req):
    """Verify the match is indeed the package we searched for.

    Some sources are not accurate in their search methods, such as
    yum, which uses regex to find a match instead of more accurate
    comparison.

    Also, requirement might be called 'hacking' while the RPM is
    'python-hacking'.
    """
    m = re.search(r'(^[a-zA-z0-9\-]*)\-\d', match)
    return m.group(1) in [prefix+req for prefix in const.PREFIXES]

def get_rpm_details(rpm):
    """Returns the name, version, os and arch of the given RPM string."""

    name = re.search(r'(^[a-zA-z0-9\-]*)\-\d', rpm)
    version = re.search(r'((\d+\.)+\d+(\-\d+))', match)
    os = re.search(r'\.([a-z]+[0-9]{1,2})', match)
    arch = re.search(r'.([a-zA-Z]+)$', match)

    return name.group(1), version.group(1), os.group(1), arch.group(1)
