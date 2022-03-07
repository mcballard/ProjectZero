"""this module contains data access for account object"""
from custom_exceptions.negative_balance import NegativeBalance
from custom_exceptions.record_not_found import RecordNotFound
from data_entities.account import Account
from data_layer.dao_package.account_DAO_interface import AccountDaoInterface


class AccountDao(AccountDaoInterface):
    account_unique_id = 1
    account_list = []

    def __init__(self):
        pass
        """
        self.account_id = default_test_account.account_id
        self.customer_id = default_test_account.customer_id
        self.account_balance = default_test_account.account_balance
        self.account_list.append(default_test_account)
        """

    def create_account(self, account_id: int, customer_id: int, account_balance: float) -> Account:
        if account_balance < 0:
            raise NegativeBalance("Cannot have negative account balance.")
        else:
            new_account = Account(self.account_unique_id, customer_id, account_balance)
            self.account_unique_id += 1
            self.account_list.append(new_account)
            return new_account

    def get_account_info_by_id(self, account_id: int) -> Account:
        for accounts in self.account_list:
            if accounts.account_id == account_id:
                return accounts
        raise RecordNotFound("Record not found.")

    def get_all_accounts_by_customer_id(self, customer_id: int) -> []:
        customer_accounts = []
        for accounts in self.account_list:
            if accounts.customer_id == customer_id:
                customer_accounts.append(accounts)
        if len(customer_accounts) != 0:
            return customer_accounts
        raise RecordNotFound("No accounts for this customer found.")

    def update_account_by_id(self, account_id: int, balance_change: float) -> Account:
        for accounts in self.account_list:
            if accounts.account_id == account_id:
                accounts.account_balance += balance_change
                return accounts
        raise RecordNotFound("Account record not found.")

    def delete_account_by_id(self, account_id: int) -> bool:
        for accounts in self.account_list:
            if accounts.account_id == account_id:
                self.account_list.remove(accounts)
                return True
        raise RecordNotFound("Record not found.")


