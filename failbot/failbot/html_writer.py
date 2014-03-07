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

# This class manages the creation of the html page from the dbbot database

import os
import datetime
from string import Template
from xml.sax.saxutils import escape

from dbbot import Logger


class HtmlWriter(object):
    template_path = os.path.abspath(__file__ + '../../../templates')

    # escape() only takes care of &, < and >
    additional_html_escapes = {
        '"': "&quot;",
        "'": "&apos;"
    }

    def __init__(self, db, output_file_path, report_title, verbose_stream):
        self._verbose = Logger('HTML', verbose_stream)
        self._db = db
        self._output_file_path = output_file_path
        self._report_title = report_title
        self._init_layouts()

    def _init_layouts(self):
        self._verbose('- Loading HTML templates')
        self._full_layout = self._read_template('layout.html')
        self._three_column_table_layout = self._read_template('three_column_table.html')
        self._three_column_row_layout = self._read_template('three_column_row.html')
        self._two_column_table_layout = self._read_template('two_column_table.html')
        self._two_column_row_layout = self._read_template('two_column_row.html')

    def _read_template(self, filename):
        with open(os.path.join(self.template_path, filename), 'r') as file:
            content = file.read()
        return Template(content)

    def produce(self):
        self._verbose('- Producing summaries from database')
        output_html = self._full_layout.substitute({
            'page_title': self._report_title,
            'time_stamp': self._return_time_string(),
            'most_failed_suites': self._table_of_most_failed_suites(),
            'most_failed_tests': self._table_of_most_failed_tests(),
            'most_failed_keywords': self._table_of_most_failed_keywords()
        })
        self._write_file(self._output_file_path, output_html)

    def _write_file(self, filename, content):
        self._verbose('- Writing %s' % filename)
        with open(filename, 'w') as file:
            file.write(content)

    def _table_of_most_failed_suites(self):
        return self._format_two_column_table(self._db.most_failed_suites())

    def _table_of_most_failed_tests(self):
        return self._format_three_column_table_with_suite_name(self._db.most_failed_tests())

    def _table_of_most_failed_keywords(self):
        return self._format_two_column_table(self._db.most_failed_keywords())

    def _format_three_column_table(self, rows):
        return self._three_column_table_layout.substitute({
            'rows': ''.join([self._format_three_column_row(row) for row in rows])
        })

    def _format_three_column_table_with_suite_name(self, rows):
        return self._three_column_table_layout.substitute({
            'rows': ''.join([self._format_three_column_row_with_suite_name(row) for row in rows])
        })

    def _format_three_column_row(self, item):
        return self._three_column_row_layout.substitute({
            'name': self._escape(item[1]),
            'suite_name': '',
            'count': item[0]
        })

    def _format_three_column_row_with_suite_name(self, item):
        return self._three_column_row_layout.substitute({
            'suite_name': self._escape(item[2]),
            'name': self._escape(item[1]),
            'count': item[0]
        })

    def _format_two_column_table(self, rows):
        return self._two_column_table_layout.substitute({
            'rows': ''.join([self._format_two_column_row(row) for row in rows])
        })

    def _format_two_column_table_with_suite_name(self, rows):
        return self._two_column_table_layout.substitute({
            'rows': ''.join([self._format_three_column_row_with_suite_name(row) for row in rows])
        })

    def _format_two_column_row(self, item):
        return self._two_column_row_layout.substitute({
            'name': self._escape(item[1]),
            'suite_name': '',
            'count': item[0]
        })

    def _format_two_column_row_with_suite_name(self, item):
        return self._two_column_row_layout.substitute({
            'name': self._escape(item[1]),
            'count': item[0]
        })

    def _escape(self, text):
        return escape(text, self.additional_html_escapes)

    def _return_time_string(self):
        current_date = datetime.datetime.now()
        date_as_string = str(current_date)

        return "Report generated at %s" % date_as_string
