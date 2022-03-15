from custom_exceptions.record_not_found import RecordNotFound
from data_entities.customer import Customer
from data_entities.account import Account
from data_layer.dao_package.db_access_for_data_layer import create_table_row_entry, select_table_record, \
    select_all_table_records_by_id, update_table_record, delete_table_record, truncate_tables


test_customer = Customer(0, "Matt", "Ballard")
test_customer_update = Customer(4, "Matt", "Changed")
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
    result = update_table_record(test_customer_update)
    assert result


def test_delete_record_by_id_success():
    result = delete_table_record(2, test_customer.class_name)
    assert result


def test_delete_record_by_id_does_not_exist():
    try:
        result = delete_table_record(35, test_customer.class_name)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_select_all_records_no_records():
    try:
        this_should_fail = Customer(-1, "doesnt", "matter")
        result = select_all_table_records_by_id(this_should_fail)
        assert False
    except RecordNotFound as e:
        assert str(e) == "No records found."


def test_truncate_tables():
    assert truncate_tables() != 0
