from custom_exceptions.corrupt_transaction_db import CorruptedTransactionAborted
from custom_exceptions.record_not_found import RecordNotFound
from data_entities.customer import Customer
from data_entities.account import Account
from data_layer.dao_package.db_access_for_data_layer import DBAccessObject

test_db_access_object = DBAccessObject()

test_customer = Customer(0, "Matt", "Ballard")
test_customer_update = Customer(4, "Matt", "Changed")
test_account = Account(0, 2, 15000)


def test_insert_record_success():
    assert test_db_access_object.create_table_row_entry(test_customer).customer_id != 0


def test_select_record_by_id_success():
    assert test_db_access_object.select_table_record(4, test_customer.table_name).customer_id == 4


def test_select_record_by_id_does_not_exist():
    try:
        return_object = test_db_access_object.select_table_record(1000, test_customer.table_name)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_select_all_records_success():
    assert len(test_db_access_object.select_all_table_records_by_id(test_customer_update)) >= 1


def test_update_record_success():
    result = test_db_access_object.update_table_record(test_customer_update)
    assert result


def test_delete_record_by_id_success():
    result = test_db_access_object.delete_table_record(2, test_customer.table_name)
    assert result


def test_transfer_success():
    account1 = Account(7, 4, 14000)
    account2 = Account(8, 4, 16000)
    result = test_db_access_object.update_multiple_related_records(account1, account2)
    assert result[0].account_balance == 14000


def test_transfer_failure():
    incorrect_account_info = Account(8, 4, 15000)
    incorrect_account_info2 = Account(-1, 4, 15000)
    try:
        result = test_db_access_object.update_multiple_related_records(incorrect_account_info, incorrect_account_info2)
        assert False
    except CorruptedTransactionAborted as e:
        assert str(e) == "The transfer could not be completed."


def test_delete_record_by_id_does_not_exist():
    try:
        result = test_db_access_object.delete_table_record(35, test_customer.table_name)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_select_all_records_no_records():
    try:
        this_should_fail = Customer(-1, "doesnt", "matter")
        result = test_db_access_object.select_all_table_records_by_id(this_should_fail)
        assert False
    except RecordNotFound as e:
        assert str(e) == "No records found."


def test_truncate_tables():
    assert test_db_access_object.truncate_tables() != 0
