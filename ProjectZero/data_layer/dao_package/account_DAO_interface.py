"""this module contains the interface for the account data access object"""
from abc import ABC, abstractmethod

from data_entities.account import Account


class AccountDaoInterface(ABC):

    @abstractmethod
    def create_account(self, account_id: int, customer_id: int, account_balance: float) -> Account:
        pass

    @abstractmethod
    def get_account_info_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts_by_customer_id(self, customer_id: int) -> []:
        pass

    @abstractmethod
    def update_account_by_id(self, account_id: int, balance_change: float) -> Account:
        pass

    @abstractmethod
    def delete_account_by_id(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def transfer_to_account(self, from_account: Account, to_account: Account, amount_to_transfer: float) -> []:
        pass

"""
    @abstractmethod
    def deposit_to_account(self, account: Account, amount_to_deposit: float) -> Account:
        pass

    @abstractmethod
    def withdraw_from_account(self, account: Account, amount_to_withdraw: float) -> Account:
        pass

"""
