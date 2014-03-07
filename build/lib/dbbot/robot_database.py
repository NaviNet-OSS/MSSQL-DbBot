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

# This class manages the connection to the database

import pymssql

from .logger import Logger


class RobotDatabase(object):

    def __init__(self, verbose):
        self._verbose = Logger('Database', verbose)
        self._connection = self._connect()

    def _connect(self):
        self._verbose('- Establishing database connection')
        return pymssql.connect(host='SQL.SERVER.HOST', user='exampleusername', password='password', database='RobotDB')

    def close(self):
        self._verbose('- Closing database connection')
        self._connection.close()
