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

import argparse


def create_parser():
    """Returns argument parser"""

    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('--debug', action='store_true',
                        dest="debug", help='debug flag')

    parser.add_argument('-c', '--convert-only', action='store_true',
                        dest='convert',
                        help='Convert pip packages to simple RPMs list')

    parser.add_argument('--copr', dest='copr_projects', nargs='+',
                        help='Copr projects')

    parser.add_argument('--long', action='store_true', dest='long',
                        help='Use RPM long version(e.g 1.2.1-3)')

    parser.add_argument('-r', '--reqs', dest='reqs',
                        help="Requirements files")

    parser.add_argument('-m', '--missing', action='store_true',
                        dest='missing',
                        help="Show only missing packages")

    return parser
