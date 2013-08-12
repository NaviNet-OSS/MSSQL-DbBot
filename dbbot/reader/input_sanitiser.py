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
