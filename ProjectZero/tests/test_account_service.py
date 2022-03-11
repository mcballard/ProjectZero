"""this module contains testing for the service layer account interactions"""
from custom_exceptions.customer_id_mismatch import CustomerIdMismatch
from custom_exceptions.incorrect_data_field import IncorrectDataField
from custom_exceptions.negative_balance import NegativeBalance
from custom_exceptions.record_not_found import RecordNotFound
from data_layer.dao_package.account_dao import AccountDao
from service_layer.service_layer_package.account_service_implementation import AccountSlImp

account_dao_test_object = AccountDao()
account_sl_test_object = AccountSlImp(account_dao_test_object)

# positive tests


def test_create_account_success_sl():
    result = account_sl_test_object.sl_create_account(0, 9001)
    assert result.account_id != 0


def test_leave_bank_by_customer_id_success_sl():
    all_closed = account_sl_test_object.sl_leave_bank_by_customer_id(6)
    assert all_closed[0]


def test_leave_bank_customer_id_record_not_found_sl():
    try:
        all_closed = account_sl_test_object.sl_close_account_by_id(1000)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Record not found."


def test_close_account_by_id_record_not_found_sl():
    try:
        is_removed = account_sl_test_object.sl_close_account_by_id(8, 1)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_deposit_to_account_success_sl():
    result = account_sl_test_object.deposit_to_account_by_id(12, 1000)
    assert result.account_id == 12


def test_withdraw_from_account_success_sl():
    result = account_sl_test_object.withdraw_from_account_by_id(account_dao_test_object.account_list[1].account_id, account_dao_test_object.account_list[1].customer_id, 500.5)
    assert result.account_balance == 999.5


def test_transfer_to_account_from_account_success_sl():
    result = account_sl_test_object.transfer_to_account(account_dao_test_object.account_list[1], account_dao_test_object.account_list[2], 100)
    assert result[0].account_balance == 899.5


def test_transfer_to_account_to_account_success_sl():
    result = account_sl_test_object.transfer_to_account(account_dao_test_object.account_list[2], account_dao_test_object.account_list[1], 100)
    assert result[1].account_balance == 999.5


# negative tests


def test_deposit_to_account_record_does_not_exist_sl():
    try:
        result = account_sl_test_object.deposit_to_account_by_id(-1, 1000)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_withdraw_from_account_customer_id_mismatch():
    try:
        result = account_sl_test_object.withdraw_from_account_by_id(1, 2, 0)
        assert False
    except CustomerIdMismatch as e:
        assert str(e) == "You cannot withdraw from another customer's account."


def test_create_account_non_int_id_sl():
    try:
        result = account_sl_test_object.sl_create_account("test", 1000)
        assert False
    except IncorrectDataField as e:
        assert str(e) == "The customer id must be an integer."


def test_create_account_with_zero_customer_id():
    try:
        result = account_sl_test_object.sl_create_account(0, 9000)
        assert False
    except IncorrectDataField as e:
        assert str(e) == "Must have customer id to connect to account."


def test_create_account_non_number_balance_sl():
    try:
        result = account_sl_test_object.sl_create_account(1, "1000")
        assert False
    except IncorrectDataField as e:
        assert str(e) == "The account balance must be a number."


def test_transfer_negative_balance_sl():
    try:
        result = account_sl_test_object.transfer_to_account(12, 2, 30000)
        assert False
    except NegativeBalance as e:
        assert str(e) == "You cannot overdraw your account."


def test_withdraw_negative_balance_sl():
    try:
        result = account_sl_test_object.withdraw_from_account_by_id(12, 2, 30000)
        assert False
    except NegativeBalance as e:
        assert str(e) == "You do not have sufficient funds."


def test_withdraw_a_negative_amount():
    try:
        result = account_sl_test_object.withdraw_from_account_by_id(37, 2, -5000)
        assert False
    except IncorrectDataField as e:
        assert str(e) == "Cannot withdraw a negative amount."


# will fail unless updated
def test_delete_account_by_account_id_success_sl():
    is_removed = account_sl_test_object.sl_delete_account_by_account_id(5)
    assert is_removed is True


# will fail unless updated
def test_close_account_by_id_success_sl():
    is_removed = account_sl_test_object.sl_close_account_by_id(11)
    assert is_removed[0] is True

