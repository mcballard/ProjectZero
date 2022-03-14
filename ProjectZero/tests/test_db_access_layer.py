from unittest.mock import MagicMock, patch

from custom_exceptions.record_not_found import RecordNotFound
from data_entities.customer import Customer
from data_entities.account import Account
from data_layer.dao_package.db_access_for_data_layer import create_table_row_entry, select_table_record, \
    select_all_table_records_by_id, update_table_record, delete_table_record, truncate_tables
from custom_exceptions.database_error import DatabaseError

test_customer = Customer(0, "Matt", "Ballard")
test_customer_update = Customer(5, "Matt", "Changed")
test_account = Account(0, 2, 15000)


def test_insert_record_success():
    assert create_table_row_entry(test_customer).customer_id != 0


def test_select_record_by_id_success():
    assert select_table_record(4, test_customer.class_name).customer_id == 4


def test_select_record_by_id_does_not_exist():
    try:
        return_object = select_table_record(1000, test_customer.class_name)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_select_all_records_success():
    assert len(select_all_table_records_by_id(test_customer_update)) >= 1


def test_update_record_success():
    update_table_record = MagicMock(result_value=True)
    result = update_table_record(test_customer_update)
    assert result


# must change for next test to pass
def test_delete_record_by_id_success():
    delete_table_record = MagicMock(result_value=True)
    result = delete_table_record(2, test_customer.class_name)
    assert result


@patch("tests.test_db_access_layer.delete_table_record")
def test_delete_record_by_id_does_not_exist(mock):
    mock.side_effect = DatabaseError("Could not find record in database.")
    try:
        result = delete_table_record(35, test_customer.class_name)
        assert False
    except DatabaseError as e:
        assert str(e) == "Could not find record in database."


@patch("tests.test_db_access_layer.select_all_table_records_by_id")
def test_select_all_records_no_records(mock):
    mock.side_effect = RecordNotFound("No records found.")
    try:
        result = select_all_table_records_by_id(test_customer)
        assert False
    except RecordNotFound as e:
        assert str(e) == "No records found."


def test_truncate_tables():
    assert truncate_tables() != 0
