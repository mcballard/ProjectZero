from ast import literal_eval
from re import sub

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
        return snake_case_dictionary

    def create_record_business_logic_data_manipulation(self, row_object_from_api: TestRowObject) -> dict:
        # business logic must be implemented here before passing the object information to db access object
        result_set = self.db_access_object.select_record(row_object_from_api.return_insert_single_record_query_sql())
        comma_count = 0
        result_nested_dictionary_concat = ""
        if len(result_set) > 1:
            for record in result_set:
                comma_count += 1
                result_nested_dictionary_concat += "'tableRow" + str(record.unique_id) + "':" + str(
                    record.return_dictionary_for_json())
                if comma_count < len(record):
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

test_convert = {
    "thisIsATest": "blah",
    "thisIsATest2": "blah",
    "thisIsATest3": "blah",
    "thisIsATest4": "blah"
}

test_dao = TestingDBAccessObject()
test_object = TestServiceLayerImplementation(test_dao)

print(test_object.sanitize_json_from_api(test_convert))
