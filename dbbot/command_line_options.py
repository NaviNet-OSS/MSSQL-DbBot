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
