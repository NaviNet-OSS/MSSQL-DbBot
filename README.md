MSSQL DbBot
=====

This is a forked version of DbBot, which is a Python script to serialize Robot Framework produced test run results, i.e. output.xml files, into a database. This version serializes the results into a Microsoft® SQL Server database to provide the future Robot Framework related tools and plugins with a unified storage for the test run results.


Requirements
------------
* Python 2.6 or newer installed
* Robot Framework 2.7 or newer installed
* Pymssql 2.7 installed. The downloads can be found [here](http://code.google.com/p/pymssql/downloads/list) 

Robot Framework version 2.7.4 or later is recommended as versions prior to 2.7.4 do not support storing total elapsed time for test runs or tags.

Further information
------------

https://github.com/NaviNet/MSSQL-DbBot/wiki


License
-------
MSSQL-DbBot is released under the [MIT License](http://www.tldrlegal.com/license/mit-license).

See LICENSE.TXT for details.
