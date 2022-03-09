from custom_exceptions.record_not_found import RecordNotFound
from data_entities.customer import Customer
from data_entities.account import Account
from data_layer.dao_package.db_access_for_data_layer import create_customer_entry, select_customer_record, \
    select_all_customer_records, update_customer_record, delete_customer_record
from custom_exceptions.database_error import DatabaseError

test_customer = Customer(0, "Matt", "Ballard")
test_customer_update = Customer(5, "Matt", "Changed")
test_account = Account(0, 2, 15000)


def test_insert_record_success():
    assert create_customer_entry(test_customer).customer_id != 0


def test_select_record_by_id_success():
    assert select_customer_record(3, test_customer.class_name).first_name == "Matt"


def test_select_record_by_id_does_not_exist():
    try:
        return_object = select_customer_record(1000, test_customer.class_name).first_name == "Matt"
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_select_all_records_success():
    assert len(select_all_customer_records(test_customer_update)) >= 1


def test_update_record_success():
    assert update_customer_record(test_customer_update).last_name == "Changed"


# must change for next test to pass
def test_delete_record_by_id_success():
    assert delete_customer_record(11, test_customer.class_name)


def test_delete_record_by_id_does_not_exist():
    try:
        result = select_customer_record(35, test_customer.class_name).first_name == "Matt"
    except DatabaseError as e:
        assert str(e) == "Could not find record in database."


def test_select_all_records_no_records():
    try:
        result = select_all_customer_records(test_customer)
    except RecordNotFound as e:
        assert str(e) == "No Records Found."
