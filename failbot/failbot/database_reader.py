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
# This class contains the failbot selection statements and execution command

from dbbot import RobotDatabase


class DatabaseReader(RobotDatabase):

    def __init__(self, verbose_stream):
        super(DatabaseReader, self).__init__(verbose_stream)

    def most_failed_suites(self):
        sql_statement = '''
            SELECT count(suites.id) as count, suites.name, suites.id, suites.source
            FROM suites, suite_status
            WHERE suites.id = suite_status.suite_id AND
            suite_status.status = 'FAIL'
            GROUP BY suites.source, suites.id, suites.name
            ORDER BY count DESC
        '''
        return self._fetch_by(sql_statement)

    def most_failed_tests(self):
        sql_statement = '''
            SELECT count(tests.id) as count, tests.name, suites.name, tests.id
            FROM tests, test_status, suites
            WHERE tests.id = test_status.test_id
			AND tests.suite_id = suites.id
            AND test_status.status = 'FAIL'
            GROUP BY tests.name, tests.suite_id, tests.id, suites.name
            ORDER BY count DESC
        '''
        return self._fetch_by(sql_statement)

    def most_failed_keywords(self):
        sql_statement = '''
            SELECT count(keywords.id) as count, keywords.name, keywords.type
            FROM keywords, keyword_status
            WHERE keywords.id = keyword_status.keyword_id
            AND keyword_status.status = 'FAIL'
            GROUP BY keywords.name, keywords.type
            ORDER BY count DESC
        '''
        return self._fetch_by(sql_statement)

    def failed_tests_for_suite(self, suite_id):
        sql_statement = '''
            SELECT count(tests.id) as count, tests.name, tests.id, tests.suite_id
            FROM tests, test_status
            WHERE tests.id = test_status.test_id
            AND tests.suite_id = %s
            AND test_status.status = 'FAIL'
            GROUP BY tests.name, tests.id, tests.suite_id
            ORDER BY count DESC
        '''
        return self._fetch_by(sql_statement, [suite_id])

    def failed_keywords_for_test(self, test_id):
        sql_statement = '''
            SELECT count(keywords.id) as count, keywords.name, keywords.type
            FROM keywords, keyword_status
            WHERE keywords.id = keyword_status.keyword_id
            AND keywords.test_id = %s
            AND keyword_status.status = 'FAIL'
            GROUP BY keywords.name, keywords.type
            ORDER BY count DESC
        '''
        return self._fetch_by(sql_statement, [test_id])

    def _fetch_by(self, sql_statement, values=[]):
        cursor = self._connection.cursor()
        cursor.execute(sql_statement, values)

        return cursor.fetchall()

