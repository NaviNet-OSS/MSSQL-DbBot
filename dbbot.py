#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.abspath(__file__ + '/../..'))
from dbbot.reader import DatabaseWriter, ReaderOptions, RobotResultsParser
from robot.errors import DataError


class DbBot(object):

    def __init__(self):
        self._options = ReaderOptions()
        verbose_stream = sys.stdout if self._options.be_verbose else None
        self._db = DatabaseWriter(verbose_stream)
        self._parser = RobotResultsParser(
            self._options.include_keywords,
            self._options.log_messages,
            self._db,
            verbose_stream
        )

    def run(self):
        try:

            if self._options.clear_database:
                self._db.clear_database() 

            for xml_file in self._options.file_paths:
                self._parser.xml_to_db(xml_file)
                self._commit()

        except DataError, message:
            sys.stderr.write('dbbot: error: Invalid XML: %s\n\n' % message)
            exit(1)
        finally:
            self._db.close()
    
    def _commit(self):
        if self._options.dry_run:
            print "Dry-run: skip database commit"
        else:
            self._db.commit()

if __name__ == '__main__':
    DbBot().run()
