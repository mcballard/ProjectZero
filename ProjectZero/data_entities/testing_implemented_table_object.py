from custom_exceptions.incomplete_column_dictionary import IncompleteColumnDictionary


class TestRowObject:

    def __init__(self, row_columns_with_values: dict):
        # the dictionary object is ideally constructed using information from a RESTful api
        # it is then converted to whichever convention is used in the database and code in this case snake_case
        # /table_name/<unique_id>/foreign_table_name/<foreign_key>
        # using this as a basic structure example, while the foreign_key is shown it is not a
        # part of the minimum key values required, rather only a guideline for adding relationships
        # at a minimum a unique_id preferably a primary key relationship in the table and the name of the table
        # would be required, anything else is a business case and implementation should be handled as such
        self.object_specific_attributes_dictionary = row_columns_with_values
        if self.object_specific_attributes_dictionary["table_name"] is None \
                or self.object_specific_attributes_dictionary["unique_id"] is None:
            raise IncompleteColumnDictionary("Dictionary defining minimum column requirements is incomplete.")

    def return_dictionary_for_json(self) -> dict:
        # return dictionary with proper table name and column names for specific implementations
        # with camelCase keys reflecting column names and table name
        pass

    def return_dictionary_for_sql(self) -> dict:
        # return dictionary with proper table name and column names for specific implementations
        pass

    def return_insert_single_record_query_sql(self) -> str:
        # should return a simple insert query for specific instance of object with correct column information
        # and table name in order to create new record based on a normalized table
        commas = 0
        sql_query = "insert into"+str(self.object_specific_attributes_dictionary["table_name"])+" values(default,"
        for key, values in self.object_specific_attributes_dictionary:
            commas += 1
            if key != "table_name" or key != "unique_id":
                sql_query += str(self.object_specific_attributes_dictionary[values])
                if commas < len(self.object_specific_attributes_dictionary):
                    sql_query += ","
        sql_query += ") returning *;"
        return sql_query

    def return_select_single_record_query_sql(self) -> str:
        # should return a simple select * query for specific instance of object with correct primary key
        pass

    def return_update_single_record_query_sql(self) -> str:
        # should return a simple update for specific instance of object with correct primary key
        pass

    def return_delete_single_record_query_sql(self) -> str:
        # should return a simple delete query for specific instance of object with correct primary key
        pass
