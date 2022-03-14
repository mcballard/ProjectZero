"""this module contains the implementation of the service level account interactions"""
import operator
from custom_exceptions.customer_id_mismatch import CustomerIdMismatch
from custom_exceptions.incorrect_data_field import IncorrectDataField
from custom_exceptions.negative_balance import NegativeBalance
from custom_exceptions.record_not_found import RecordNotFound
from data_entities.account import Account
from data_layer.dao_package.account_DAO_interface import AccountDaoInterface
from service_layer.service_layer_package.account_service_interface import AccountSlInterface


class AccountSlImp(AccountSlInterface):

    def __init__(self, account_dao: AccountDaoInterface):
        self.account_dao = account_dao

    def sl_create_account(self, customer_id: int, account_balance: float) -> Account:
        if type(customer_id) != int:
            raise IncorrectDataField("The customer id must be an integer.")
        elif (type(account_balance) != int) and (type(account_balance) != float):
            #  0 is used as placeholder for account_id in creating new account
            raise IncorrectDataField("The account balance must be a number.")
        elif customer_id <= 0:
            raise IncorrectDataField("Must have customer id to connect to account.")
        return self.account_dao.create_account(0, customer_id, account_balance)

    def sl_get_account_info_by_id(self, account_id: int, customer_id: int) -> Account:
        if type(account_id) != int:
            raise IncorrectDataField("The customer id must be an integer.")
        if self.account_dao.get_account_info_by_id(account_id).customer_id != customer_id:
            raise CustomerIdMismatch("You do not have access to other customer accounts.")
        return self.account_dao.get_account_info_by_id(account_id)

    def sl_get_all_accounts_by_customer_id(self, customer_id: int) -> []:
        return self.account_dao.get_all_accounts_by_customer_id(customer_id)

    def sl_update_account_by_id(self, account_id: int, balance_change: float) -> Account:
        pass  # this function isn't explicitly implemented on purpose

    def sl_delete_account_by_account_id(self, account_id: int) -> bool:
        if type(account_id) != int:
            raise IncorrectDataField("The customer id must be an integer.")
        return self.account_dao.delete_account_by_id(account_id)

    def sl_leave_bank_by_customer_id(self, customer_id: int) -> []:
        is_record_removed = False
        amount_withdrawn: float = 0
        accounts_to_close = self.sl_get_all_accounts_by_customer_id(customer_id)
        if accounts_to_close is not None:
            for accounts in accounts_to_close:
                amount_to_withdraw = accounts.account_balance
                closed_account = self.withdraw_from_account_by_id(accounts.account_id, accounts.customer_id, amount_to_withdraw)
                amount_withdrawn += amount_to_withdraw
                is_record_removed = self.sl_delete_account_by_account_id(closed_account.account_id)
        if is_record_removed and (amount_withdrawn != 0):
            return True, amount_withdrawn
        else:
            raise RecordNotFound("No accounts closed.")

    def sl_close_account_by_id(self, account_id: int, customer_id: int) -> []:
        account_to_close = self.sl_get_account_info_by_id(account_id, customer_id)
        if account_to_close.customer_id != customer_id:
            raise CustomerIdMismatch("You cannot access someone else's accounts.")
        amount_to_withdraw = account_to_close.account_balance
        closed_account = self.withdraw_from_account_by_id(account_to_close.account_id, account_to_close.customer_id, amount_to_withdraw)
        self.sl_delete_account_by_account_id(account_id)
        is_record_removed = True
        if is_record_removed and (closed_account.account_balance == 0):
            return True, amount_to_withdraw
        raise RecordNotFound("Record not found.")

    def deposit_to_account_by_id(self, account_id: int, amount_to_change: float) -> Account:
        if amount_to_change < 0:
            raise IncorrectDataField("Cannot deposit negative amount.")
        current_account = self.account_dao.get_account_info_by_id(account_id)
        if operator.is_(current_account.account_id, account_id):
            account_to_change = self.account_dao.get_account_info_by_id(account_id)
            updated_account = self.account_dao.update_account_by_id(account_to_change.account_id, amount_to_change)
            return updated_account
        raise RecordNotFound("Account not found.")

    def withdraw_from_account_by_id(self, account_id: int, customer_id, amount_to_change: float) -> Account:
        if amount_to_change >= 0:
            current_account = self.account_dao.get_account_info_by_id(account_id)
            if operator.lt(current_account.account_balance, amount_to_change):
                raise NegativeBalance("You do not have sufficient funds.")
            elif operator.is_not(current_account.customer_id, customer_id):
                raise CustomerIdMismatch("You cannot withdraw from another customer's account.")
            else:
                account_to_change = self.account_dao.get_account_info_by_id(account_id)
                updated_account = self.account_dao.update_account_by_id(account_to_change.account_id, -amount_to_change)
                return updated_account
        raise IncorrectDataField("Cannot withdraw a negative amount.")

    def transfer_to_account(self, from_account: Account, to_account: Account, amount_to_transfer: float) -> []:
        returned_accounts = []
        if from_account.account_balance.__lt__(amount_to_transfer):
            raise NegativeBalance("You cannot overdraw your account.")
        else:
            withdrawn_account = self.withdraw_from_account_by_id(from_account.account_id, from_account.customer_id, amount_to_transfer)
            returned_accounts.append(withdrawn_account)
            deposited_account = self.deposit_to_account_by_id(to_account.account_id, amount_to_transfer)
            returned_accounts.append(deposited_account)
        return returned_accounts
