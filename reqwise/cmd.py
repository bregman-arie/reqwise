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
import sys

from manager import Manager
import parse


def setup_logging(debug):
    """Sets the logging."""
    format = '%(message)s'
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format=format)


def main():
    """Reqwise Main Entry."""

    # Parse arguments provided by the user
    parser = parse.create_parser()
    args = parser.parse_args()

    setup_logging(args.debug)

    # Create and start reqwise manager
    manager = Manager(args)
    manager.start()


if __name__ == '__main__':
    sys.exit(main())
