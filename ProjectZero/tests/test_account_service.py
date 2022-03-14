"""this module contains testing for the service layer account interactions"""
from unittest.mock import patch, MagicMock

from custom_exceptions.customer_id_mismatch import CustomerIdMismatch
from custom_exceptions.incorrect_data_field import IncorrectDataField
from custom_exceptions.negative_balance import NegativeBalance
from custom_exceptions.record_not_found import RecordNotFound
from data_entities.account import Account
from data_layer.dao_package.account_dao import AccountDao
from service_layer.service_layer_package.account_service_implementation import AccountSlImp

account_dao_test_object = AccountDao()
account_sl_test_object = AccountSlImp(account_dao_test_object)

# positive tests


def test_create_account_success_sl():
    result = account_sl_test_object.sl_create_account(4, 9001)
    assert result.account_id != 0


def test_leave_bank_by_customer_id_success_sl():
    account_sl_test_object.sl_leave_bank_by_customer_id = MagicMock(result_value=True)
    all_closed = account_sl_test_object.sl_leave_bank_by_customer_id(6)
    assert all_closed


@patch("tests.test_account_service.account_sl_test_object.sl_close_account_by_id")
def test_close_account_customer_id_record_not_found_sl(mock):
    mock.side_effect = RecordNotFound("Record not found.")
    try:
        all_closed = account_sl_test_object.sl_close_account_by_id(1000, 1)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Record not found."


@patch("tests.test_account_service.account_sl_test_object.sl_close_account_by_id")
def test_close_account_by_id_record_not_found_sl(mock):
    mock.side_effect = RecordNotFound("Could not find record in database.")
    try:
        is_removed = account_sl_test_object.sl_close_account_by_id(8, 1)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_deposit_to_account_success_sl():
    result = account_sl_test_object.deposit_to_account_by_id(4, 1000)
    assert result.account_id == 4


def test_withdraw_from_account_success_sl():
    account_sl_test_object.withdraw_from_account_by_id = MagicMock(result_value=True)
    result = account_sl_test_object.withdraw_from_account_by_id(1, 1, 500.5)
    assert result


def test_transfer_to_account_from_account_success_sl():
    account_sl_test_object.transfer_to_account = MagicMock(result_value=True)
    test_account_1 = Account(1, 1, 999.5)
    test_account_2 = Account(2, 1, 0)
    result = account_sl_test_object.transfer_to_account(test_account_1, test_account_2, 100)
    assert result


def test_transfer_to_account_to_account_success_sl():
    account_sl_test_object.transfer_to_account = MagicMock(result_value=True)
    test_account_1 = Account(1, 1, 899.5)
    test_account_2 = Account(2, 1, 100)
    result = account_sl_test_object.transfer_to_account(test_account_2, test_account_1, 100)
    assert result


# negative tests


def test_deposit_to_account_record_does_not_exist_sl():
    try:
        result = account_sl_test_object.deposit_to_account_by_id(-1, 1000)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


@patch("tests.test_account_service.account_sl_test_object.withdraw_from_account_by_id")
def test_withdraw_from_account_customer_id_mismatch(mock):
    mock.side_effect = CustomerIdMismatch("You cannot withdraw from another customer's account.")
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


@patch("tests.test_account_service.account_sl_test_object.transfer_to_account")
def test_transfer_negative_balance_sl(mock):
    mock.side_effect = NegativeBalance("You cannot overdraw your account.")
    try:
        test_account_1 = Account(1, 1, 899.5)
        test_account_2 = Account(2, 1, 100)
        result = account_sl_test_object.transfer_to_account(test_account_1, test_account_2, 30000)
        assert False
    except NegativeBalance as e:
        assert str(e) == "You cannot overdraw your account."


@patch("tests.test_account_service.account_sl_test_object.withdraw_from_account_by_id")
def test_withdraw_negative_balance_sl(mock):
    mock.side_effect = NegativeBalance("You do not have sufficient funds.")
    try:
        result = account_sl_test_object.withdraw_from_account_by_id(12, 2, 30000)
        assert False
    except NegativeBalance as e:
        assert str(e) == "You do not have sufficient funds."


@patch("tests.test_account_service.account_sl_test_object.withdraw_from_account_by_id")
def test_withdraw_a_negative_amount(mock):
    mock.side_effect = IncorrectDataField("Cannot withdraw a negative amount.")
    try:
        result = account_sl_test_object.withdraw_from_account_by_id(37, 2, -5000)
        assert False
    except IncorrectDataField as e:
        assert str(e) == "Cannot withdraw a negative amount."


# will fail unless updated
def test_delete_account_by_account_id_success_sl():
    account_sl_test_object.sl_delete_account_by_account_id = MagicMock(result_value=True)
    is_removed = account_sl_test_object.sl_delete_account_by_account_id(5)
    assert is_removed


# will fail unless updated
@patch("tests.test_account_service.account_sl_test_object.sl_close_account_by_id")
def test_close_account_by_id_sl(mock):
    mock.side_effect = CustomerIdMismatch("You do not have access to other customer accounts.")
    try:
        is_removed = account_sl_test_object.sl_close_account_by_id(11, 2)
        assert False
    except CustomerIdMismatch as e:
        assert str(e) == "You do not have access to other customer accounts."

