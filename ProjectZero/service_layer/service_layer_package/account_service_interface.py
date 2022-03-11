"""this modules contains the interface for the account entity and its dao"""
from abc import ABC, abstractmethod
from data_entities.account import Account


class AccountSlInterface(ABC):

    @abstractmethod
    def sl_create_account(self, customer_id: int, account_balance: float) -> Account:
        pass

    @abstractmethod
    def sl_get_account_info_by_id(self, account_id: int, customer_id: int) -> Account:
        pass

    @abstractmethod
    def sl_get_all_accounts_by_customer_id(self, customer_id: int) -> []:
        pass

    @abstractmethod
    def sl_update_account_by_id(self, account_id: int, balance_change: float) -> Account:
        pass

    @abstractmethod
    def sl_delete_account_by_account_id(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def deposit_to_account_by_id(self, account_id: int, amount_to_deposit: float) -> Account:
        pass

    @abstractmethod
    def withdraw_from_account_by_id(self, account_id: int, customer_id, amount_to_withdraw: float) -> Account:
        pass

    @abstractmethod
    def transfer_to_account(self, from_account: Account, to_account: Account, amount_to_transfer: float) -> []:
        pass
