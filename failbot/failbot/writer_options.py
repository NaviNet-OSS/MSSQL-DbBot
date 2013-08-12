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
