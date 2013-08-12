# This class handles creating tables and managing SQL statements

import unicodedata
from dbbot import RobotDatabase
from .input_sanitiser import InputSanitiser
from pymssql import IntegrityError

class DatabaseWriter(RobotDatabase):

    def __init__(self, verbose_stream):
        super(DatabaseWriter, self).__init__(verbose_stream)
        self._input_sanitiser = InputSanitiser()
        self._init_schema()

    def _init_schema(self):
        self._verbose('- Initializing database schema')
        self._create_table_test_runs()
        self._create_table_test_run_status()
        self._create_table_test_run_errors()
        self._create_table_tag_status()
        self._create_table_suites()
        self._create_table_suite_status()
        self._create_table_tests()
        self._create_table_test_status()
        self._create_table_keywords()
        self._create_table_keyword_status()
        self._create_table_messages()
        self._create_table_tags()
        self._create_table_arguments()

    def _create_table_test_runs(self):
        self._create_table('test_runs', {
            'source_file': 'varchar(320) NOT NULL',
            'started_at': 'DATETIME NOT NULL',
            'finished_at': 'DATETIME NOT NULL',
            'imported_at': 'DATETIME NOT NULL',
        }, ('source_file', 'started_at', 'finished_at'))

    def _create_table_test_run_status(self):
        self._create_table('test_run_status', {
            'test_run_id': 'INTEGER NOT NULL REFERENCES test_runs',
            'name': 'varchar(320) NOT NULL',
            'elapsed': 'INTEGER',
            'failed': 'INTEGER NOT NULL',
            'passed': 'INTEGER NOT NULL'
        }, ('test_run_id', 'name'))

    def _create_table_test_run_errors(self):
        self._create_table('test_run_errors', {
            'test_run_id': 'INTEGER NOT NULL REFERENCES test_runs',
            'level': 'varchar(320) NOT NULL',
            'timestamp': 'DATETIME NOT NULL',
            'content': 'varchar(320) NOT NULL'
        }, ('test_run_id', 'level', 'content'))

    def _create_table_tag_status(self):
        self._create_table('tag_status', {
            'test_run_id': 'INTEGER NOT NULL REFERENCES test_runs',
            'name': 'varchar(320) NOT NULL',
            'critical': 'INTEGER NOT NULL',
            'elapsed': 'INTEGER',
            'failed': 'INTEGER NOT NULL',
            'passed': 'INTEGER NOT NULL',
        }, ('test_run_id', 'name'))

    def _create_table_suites(self):
        self._create_table('suites', {
            'suite_id': 'INTEGER',
            'xml_id': 'varchar(320) NOT NULL',
            'name': 'VARCHAR(255) NOT NULL',
            'source': 'varchar(320) NOT NULL',
            'doc': 'varchar(max) NOT NULL'
        }, ('name', 'source'))

    def _create_table_suite_status(self):
        self._create_table('suite_status', {
            'test_run_id': 'INTEGER NOT NULL',
            'suite_id': 'INTEGER  NOT NULL',
            'suite_id': 'INTEGER  NOT NULL REFERENCES suites',
            'elapsed': 'INTEGER NOT NULL',
            'failed': 'INTEGER NOT NULL',
            'passed': 'INTEGER NOT NULL',
            'status': 'varchar(320) NOT NULL'
        })

    def _create_table_tests(self):
        self._create_table('tests', {
            'suite_id': 'INTEGER NOT NULL',
            'suite_id': 'INTEGER NOT NULL REFERENCES suites',
            'xml_id': 'varchar(320) NOT NULL',
            'name': 'varchar(320) NOT NULL',
            'timeout': 'varchar(320) NOT NULL',
            'doc': 'varchar(max) NOT NULL'
        }, ('suite_id', 'name'))

    def _create_table_test_status(self):
        self._create_table('test_status', {
            'test_run_id': 'INTEGER NOT NULL REFERENCES test_runs',
            'test_id': 'INTEGER  NOT NULL REFERENCES tests',
            'status': 'varchar(320) NOT NULL',
            'elapsed': 'INTEGER NOT NULL'
        })

    def _create_table_keywords(self):
        self._create_table('keywords', {
            'suite_id': 'INTEGER',
            'test_id': 'INTEGER',
            'keyword_id': 'INTEGER',
            'name': 'VARCHAR(255) NOT NULL',
            'type': 'varchar(320) NOT NULL',
            'timeout': 'varchar(320) NOT NULL',
            'doc': 'varchar(max) NOT NULL'
        }, ('name', 'type'))

    def _create_table_keyword_status(self):
        self._create_table('keyword_status', {
            'test_run_id': 'INTEGER NOT NULL REFERENCES test_runs',
            'keyword_id': 'INTEGER NOT NULL REFERENCES keywords',
            'status': 'varchar(320) NOT NULL',
            'elapsed': 'INTEGER NOT NULL'
        })

    def _create_table_messages(self):
        self._create_table('messages', {
            'keyword_id': 'INTEGER NOT NULL REFERENCES keywords',
            'level': 'varchar(320) NOT NULL',
            'timestamp': 'DATETIME NOT NULL',
            'content': 'varchar(450) NOT NULL'
        }, ('keyword_id', 'level', 'timestamp', 'content'))

    def _create_table_tags(self):
        self._create_table('tags', {
            'test_id': 'INTEGER NOT NULL REFERENCES tests',
            'content': 'varchar(320) NOT NULL'
        }, ('test_id', 'content'))

    def _create_table_arguments(self):
        self._create_table('arguments', {
            'keyword_id': 'INTEGER NOT NULL REFERENCES keywords',
            'content': 'varchar(320) NOT NULL'
        }, ('keyword_id', 'content'))


    def _create_table(self, table_name, columns, unique_columns=()):
        definitions = ['id INTEGER IDENTITY(1,1)PRIMARY KEY']

        for column_name, properties in columns.items():
            definitions.append('%s %s' % (column_name, properties))

        if unique_columns:
            unique_column_names = ', '.join(unique_columns)
            definitions.append('CONSTRAINT unique_%s UNIQUE (%s)' % (
                table_name, unique_column_names)
            )

        if_not_exists_sql_statement = "IF NOT EXISTS (SELECT [name] FROM sys.tables WHERE [name]='%s') " % (table_name)
        sql_statement = if_not_exists_sql_statement + 'CREATE TABLE %s (%s)' % (table_name, ', '.join(definitions))

        cursor = self._connection.cursor()
        cursor.execute(sql_statement)

    def fetch_id(self, table_name, criteria):
        cursor = self._connection.cursor()

        sql_statement = 'SELECT id FROM %s WHERE ' % table_name
        sql_statement += ' AND '.join('%s=' % key + """%s""" for key in criteria.keys())

        values_as_strings = self._input_sanitiser.values_as_strings(criteria.values())
        values_as_tuple = tuple(values_as_strings)

        cursor.execute(sql_statement, values_as_tuple)
        return cursor.fetchone()[0]

    def insert(self, table_name, criteria):

        sql_statement = self._format_insert_statement(table_name, criteria.keys())
        cursor = self._connection.cursor()

        values_as_strings = self._input_sanitiser.values_as_strings(criteria.values()) 
        values_as_tuple = tuple(values_as_strings)

        cursor.execute(sql_statement, values_as_tuple)
        return cursor.lastrowid

    def insert_or_ignore(self, table_name, criteria):
        sql_statement = self._format_insert_statement(table_name, criteria.keys(), 'IGNORE')
        cursor = self._connection.cursor()
        
        values_as_strings = self._input_sanitiser.values_as_strings(criteria.values())

        cursor.execute(sql_statement, tuple(values_as_strings+values_as_strings))

    def insert_many_or_ignore(self, table_name, column_names, values):
        sql_statement = self._format_insert_statement(table_name, column_names, 'IGNORE')
        cursor = self._connection.cursor()
        
        doubled_values = []
        
        for value in values:
            list_as_tuple = tuple(self._input_sanitiser.values_as_strings(list(value)))
            doubled_values.append(list_as_tuple+list_as_tuple)

        cursor.executemany(sql_statement, doubled_values)

    def _format_insert_statement(self, table_name, column_names, on_conflict='ABORT'):
        
        parameter_list = []

        for column in column_names:
            parameter_list.append("""%s""") 

        sql_statement = 'INSERT INTO %s (%s) VALUES (%s)' % (
            table_name,
            ','.join(column_names),
            ','.join(parameter_list)
        )

        if on_conflict == 'IGNORE':
            sql_statement = self._format_insert_if_not_exists_statement(table_name, column_names, sql_statement)
     
        return sql_statement

    def _format_insert_if_not_exists_statement(self, table_name, column_names, sql_statement):
        where_param_list = []
        for i in range(len(column_names)):
            where_param_list.append(column_names[i] + " = " + """%s""")

        sql_statement_prefix = 'If Not Exists(SELECT * FROM %s WHERE %s) BEGIN ' % (
                table_name,
                " AND ".join(where_param_list)
            )

        sql_statement = sql_statement_prefix + sql_statement + " END"

        return sql_statement
      

    def clear_database(self):
        cursor = self._connection.cursor()
        tables = ('arguments', 'keyword_status', 'suite_status', 'test_run_status', 'test_status', 
                  'tag_status', 'messages','tags', 'test_run_errors', 'keywords', 'tests',
                  'suites', 'test_runs')

        self._verbose(' - Deleting rows from tables')

        for table in tables:
            sql_statement = 'DELETE FROM %s' % table
            self._verbose(' -> Clearing table: %s' % table)
            cursor.execute(sql_statement)
            
    def commit(self):
        self._verbose('- Committing changes into database')
        self._connection.commit()
