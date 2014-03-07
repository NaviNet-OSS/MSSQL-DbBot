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

# This class contains the command line options specific to failbot

from os.path import exists
from sys import argv

from dbbot import CommandLineOptions


class WriterOptions(CommandLineOptions):

    @property
    def output_file_path(self):
        return self._options.output_file_path

    @property
    def report_title(self):
        return self._options.report_title

    def _add_parser_options(self):
        super(WriterOptions, self)._add_parser_options()
        self._add_output_option()
        self._add_title_option()

    def _add_output_option(self):
        self._parser.add_option('-o', '--output',
            dest='output_file_path',
            help='path to the resulting html file',
        )

    def _add_title_option(self):
        self._parser.add_option('-n', '--name',
            dest='report_title',
            help='the report title',
        )

    def _get_validated_options(self):
        if len(argv) < 2:
            self._exit_with_help()
        options = super(WriterOptions, self)._get_validated_options()
        if not options.output_file_path:
            self._parser.error('output html filename is required')
        return options
