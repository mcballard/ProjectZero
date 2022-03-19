from custom_exceptions.corrupt_transaction_db import CorruptedTransactionAborted
from data_entities.testing_implemented_table_object import TestRowObject
from data_layer.dao_package.manage_connections import connection


class TestingDBAccessObject:

    def insert_record(self, sql_query: str) -> []:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        if cursor.rowcount < 1:
            connection.rollback()
            raise CorruptedTransactionAborted("No record was created at database level.")
        else:
            connection.commit()
            new_records_tuple_list = cursor.fetchall()
            object_list = []
            if len(new_records_tuple_list) != 0:
                for record in new_records_tuple_list:
                    table_row_object = TestRowObject(record)
                    object_list.append(table_row_object)
                return object_list
            else:
                raise CorruptedTransactionAborted("Record may have been created but no result was returned.")

    def select_record(self, sql_query: str) -> []:
        pass

    def update_record(self, sql_query: str) -> []:
        pass

    def delete_record(self, sql_query: str) -> []:
        pass
