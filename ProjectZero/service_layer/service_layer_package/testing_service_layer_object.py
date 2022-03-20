import re
from ast import literal_eval
from re import sub

from custom_exceptions.incorrect_data_field import IncorrectDataField
from data_entities.testing_implemented_table_object import TestRowObject
from data_layer.dao_package.testing_db_access_object import TestingDBAccessObject
from service_layer.service_layer_package.testing_service_layer_object_interface import TestServiceLayerObjectInterface


class TestServiceLayerImplementation(TestServiceLayerObjectInterface):

    def __init__(self, testing_db_access_object: TestingDBAccessObject):
        self.db_access_object = testing_db_access_object

    def sanitize_json_from_api(self, json_from_api: dict) -> dict:
        # this will change keys to snake_case and ensure they match database column names
        # this will also ensure number strings are convertible to the appropriate datatypes (i.e. ids are not words)
        # utilize regular expressions to parse the keys
        snake_case_dictionary = {}
        for key in json_from_api:
            snake_key = '_'.join(sub('([A-Z][a-z]+)', r' \1', sub('([A-Z]+)', r' \1', key.replace('-', ' '))).split()).lower()
            snake_case_dictionary[snake_key] = json_from_api[key]
        # application specific search for keys with _id should be implemented here including for checks
        # on any other number type expected key, value pairs to ensure values are convertible types
        for key in snake_case_dictionary:
            if re.search("_id", key):
                try:
                    proper_int_format = int(snake_case_dictionary[key])
                    snake_case_dictionary[key] = proper_int_format
                except ValueError as e:
                    raise IncorrectDataField("The input from the api is not convertible to integer for " + key)
        if type(snake_case_dictionary["table_name"]) is not str:
            raise IncorrectDataField("The field containing the table name is in the wrong format, must be a string.")
        # the following regular expression should be used on any string value entering the db to prevent sql injection
        snake_case_dictionary["table_name"] = re.sub("[^A-Za-z_0-9]", "", snake_case_dictionary["table_name"])
        try:
            check_for_int_as_table_name = int(snake_case_dictionary["table_name"])
            if type(check_for_int_as_table_name) is int:
                raise IncorrectDataField("The table name should not be a number")
            check_for_float_as_table_name = float(snake_case_dictionary["table_name"])
            if type(check_for_float_as_table_name) is float:
                raise IncorrectDataField("The table name should not be a number")
        except ValueError as e:
            # confirms cannot convert and is not a number normal execution should continue
            if e is ValueError:
                return snake_case_dictionary
        return snake_case_dictionary

    def create_record_business_logic_data_manipulation(self, row_object_from_api: TestRowObject) -> dict:
        # business logic must be implemented here before passing the object information to db access object
        result_set = self.db_access_object.insert_record(row_object_from_api.return_insert_single_record_query_sql())
        comma_count = 0
        too_many_commas = 0
        for commas in result_set:
            too_many_commas += 1
        result_nested_dictionary_concat = ""
        if type(result_set) is not None:
            for record in result_set:
                comma_count += 1
                result_nested_dictionary_concat += "{'tableRow" + \
                                                   str(record.object_specific_attributes_dictionary["unique_id"])\
                                                   + "':" + str(record.return_dictionary_for_json())
                if comma_count < too_many_commas:
                    result_nested_dictionary_concat += ","
            result_nested_dictionary_concat += "}"
            return literal_eval(result_nested_dictionary_concat)
        else:
            return literal_eval(result_set[0].return_dictionary_for_json())

    def select_record_business_logic_data_manipulation(self, row_object_id: int) -> dict:
        pass

    def update_record_business_logic_data_manipulation(self, row_object_from_api: TestRowObject) -> dict:
        pass

    def delete_record_business_logic_data_manipulation(self, row_object_id: int) -> bool:
        pass
