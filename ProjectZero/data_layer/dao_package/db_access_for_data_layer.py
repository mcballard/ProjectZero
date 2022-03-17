from custom_exceptions.corrupt_transaction_db import CorruptedTransactionAborted
from custom_exceptions.incorrect_data_field import IncorrectDataField
from custom_exceptions.record_not_found import RecordNotFound
from data_entities.customer import Customer
from data_entities.account import Account
from data_layer.dao_package.manage_connections import connection


class DBAccessObject:

    def __init(self):
        pass

    def create_table_row_entry(self, table_row_object):
        # create sql query
        sql_query = f"insert into {table_row_object.table_name} values(default,%s,%s) returning *"
        # create cursor object to handle query
        cursor = connection.cursor()
        # execute query
        if table_row_object.table_name == "customers":
            cursor.execute(sql_query, (table_row_object.first_name, table_row_object.last_name))
        elif table_row_object.table_name == "accounts":
            cursor.execute(sql_query, (table_row_object.customer_id, table_row_object.account_balance))
        # commit changes to database and allow table to be updated
        connection.commit()
        # end the function cursor.fetch returns a tuple for a result set
        new_object = cursor.fetchone()
        if table_row_object.table_name == "customers":
            if type(new_object) != tuple:
                raise RecordNotFound("Could not find record in database.")
            else:
                new_customer_object = Customer(*new_object)
                return new_customer_object
        elif table_row_object.table_name == "accounts":
            if type(new_object) != tuple:
                raise RecordNotFound("Could not find record in database.")
            else:
                new_account_object = Account(*new_object)
                return new_account_object

    def select_table_record(self, object_unique_id: int, table_to_access: str):
        # select does not need a commit as it is read only
        # connection will close after function returns value
        if table_to_access == "customers":
            sql_query = f"select * from {table_to_access} where customer_id = %s"
        elif table_to_access == "accounts":
            sql_query = f"select * from {table_to_access} where account_id = %s"
        else:
            sql_query = ""
            raise IncorrectDataField("Unexpected object used.")
        cursor = connection.cursor()
        # list for single value customer_id tuple for multiple customer_id
        cursor.execute(sql_query, [object_unique_id])
        # fetchone() returns the entire tuple of records
        result_object = cursor.fetchone()
        if result_object is None:
            raise RecordNotFound("Could not find record in database.")
        else:
            if table_to_access == "customers":
                result_customer_object = Customer(*result_object)
                return result_customer_object
            elif table_to_access == "accounts":
                result_account_object = Account(*result_object)
                return result_account_object

    def select_all_table_records_by_id(self, table_row_object):
        if table_row_object.table_name == "customers":
            sql_query = f"select * from {table_row_object.table_name} where customer_id = {table_row_object.customer_id}"
        elif table_row_object.table_name == "accounts":
            sql_query = f"select * from {table_row_object.table_name} where customer_id = {table_row_object.customer_id}"
        else:
            sql_query = ""
            raise IncorrectDataField("Unexpected object used.")
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result_object_records = cursor.fetchall()
        object_list = []
        if len(result_object_records) != 0:
            if table_row_object.table_name == "customers":
                for record in result_object_records:
                    customer_record = Customer(*record)
                    object_list.append(customer_record)
                return object_list
            elif table_row_object.table_name == "accounts":
                for record in result_object_records:
                    account_record = Account(*record)
                    object_list.append(account_record)
                return object_list
        raise RecordNotFound("No records found.")

    def update_multiple_related_records(self, record_list: []) -> []:
        if record_list[0].table_name == "customers":
            sql_query = f"update {record_list[0].table_name} set " \
                        f"first_name=%s, " \
                        f"last_name=%s " \
                        f"where customer_id=%s " \
                        f"returning customer_id, first_name, last_name"
            cursor = connection.cursor()
            cursor.execute(sql_query,
                           (record_list[0].first_name,
                            record_list[0].last_name,
                            record_list[0].customer_id))
            connection.commit()
            result_customer_tuple = cursor.fetchone()
            result_rows = cursor.rowcount
            if result_rows != 0:
                customer_object = Customer(*result_customer_tuple)
                return customer_object
            else:
                raise RecordNotFound("Could not find record in database.")
        elif record_list[0].table_name == "accounts":
            comma_count = 0
            sql_query = f"update {record_list[0].table_name} set account_balance = case "
            for record in record_list:
                sql_query += f"when account_id={str(record.account_id)} then {str(record.account_balance)}"
            sql_query += f" end where account_id in ("
            for record in record_list:
                comma_count += 1
                sql_query += str(record.account_id)
                if len(record_list) > comma_count:
                    sql_query += f","
            sql_query += f") returning account_id, customer_id, account_balance;"
            cursor = connection.cursor()
            cursor.execute(sql_query)
            result_object_records = cursor.fetchall()
            result_count = cursor.rowcount
            object_list = []
            if len(result_object_records) == len(record_list) and result_count == len(record_list):
                connection.commit()
                for record in result_object_records:
                    account_record = Account(*record)
                    object_list.append(account_record)
                return object_list
            else:
                connection.rollback()
                raise CorruptedTransactionAborted("The transfer could not be completed.")

    def delete_table_record(self, object_id, table_to_access):
        if table_to_access == "customers":
            sql_query = f"delete from {table_to_access} where customer_id=%s"
            cursor = connection.cursor()
            cursor.execute(sql_query, [object_id])
            result = cursor.rowcount
            connection.commit()
            if result == 1:
                return True
            else:
                raise RecordNotFound("Could not find record in database.")
        elif table_to_access == "accounts":
            sql_query = f"delete from {table_to_access} where account_id=%s"
            cursor = connection.cursor()
            cursor.execute(sql_query, [object_id])
            result = cursor.rowcount
            connection.commit()
            if result == 1:
                return True
            else:
                raise RecordNotFound("Could not find record in database.")

    # quick reset for tables for testing purposes
    def truncate_tables(self):
        sql_query = "truncate accounts, customers restart identity cascade"
        cursor = connection.cursor()
        cursor.execute(sql_query)
        rows_removed = cursor.rowcount
        connection.commit()
        return rows_removed
