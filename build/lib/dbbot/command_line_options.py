#  Copyright 2013-2014 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This class defines generic command line options

from optparse import OptionParser


class CommandLineOptions(object):
    default_db_name = 'robot_results.db'

    def __init__(self):
        self._parser = OptionParser()
        self._add_parser_options()
        self._options = self._get_validated_options()

    @property
    def be_verbose(self):
        return self._options.be_verbose

    def _add_parser_options(self):
        self._parser.add_option('-v', '--verbose',
            action='store_true',
            dest='be_verbose',
            help='be verbose about the operation'
        )

    def _get_validated_options(self):
        options, args = self._parser.parse_args()
        # if unknown are arguments given
        if args:
            self._exit_with_help()
        return options

    def _exit_with_help(self):
        self._parser.print_help()
        exit(1)
