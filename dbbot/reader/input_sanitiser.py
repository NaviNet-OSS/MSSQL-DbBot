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

# This class sanitises the input values so that MS SQL Server can handle them

import re

class InputSanitiser(object):
    
    def values_as_strings(self, values):
        valuesString = []
        dateRegularExpression = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]+:[0-9]+:[0-9]+.[0-9]+$')

        for value in values:
            
            if isinstance(value, unicode):
                value = value.encode('ascii', 'replace')

            if dateRegularExpression.match(str(value)):

                dateAsString = self._remove_micro_seconds(value)
                valuesString.append(dateAsString)

            else:

                filtered_value = self._replace_nonetype_with_empty_string(value)
                filtered_value = self._replace_boolean_with_int(filtered_value)
                valuesString.append(str(filtered_value))

        return valuesString


    def _remove_micro_seconds(self, value):
        dateAsString = str(value)
        return dateAsString[:-3]


    def _replace_nonetype_with_empty_string(self, valueToCheck):
        if valueToCheck == None:
            return str("")
        else:
            return valueToCheck


    def _replace_boolean_with_int(self, valueToCheck):
        if valueToCheck == True:
            return 1
        elif valueToCheck == False:
            return 0
        else:
            return valueToCheck
