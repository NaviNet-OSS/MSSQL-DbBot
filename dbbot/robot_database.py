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
