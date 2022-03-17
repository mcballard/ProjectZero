"""this module contains data access for account object"""
import decimal

from custom_exceptions.negative_balance import NegativeBalance
from data_entities.account import Account
from data_layer.dao_package.account_DAO_interface import AccountDaoInterface
from data_layer.dao_package.db_access_for_data_layer import DBAccessObject

db_access_object = DBAccessObject()


class AccountDao(AccountDaoInterface):

    def __init__(self):
        self.table_name = "accounts"

    def create_account(self, account_id: int, customer_id: int, account_balance: float) -> Account:
        if account_balance < 0:
            raise NegativeBalance("Cannot have negative account balance.")
        else:
            account_to_create = Account(account_id, customer_id, account_balance)
            return db_access_object.create_table_row_entry(account_to_create)

    def get_account_info_by_id(self, account_id: int) -> Account:
        return db_access_object.select_table_record(account_id, self.table_name)

    def get_all_accounts_by_customer_id(self, customer_id: int) -> []:
        customer_to_get_accounts_for = Account(0, customer_id, 0)
        return db_access_object.select_all_table_records_by_id(customer_to_get_accounts_for)

    def update_account_by_id(self, account_id: int, balance_change: float) -> Account:
        account_update_info: Account = db_access_object.select_table_record(account_id, self.table_name)
        account_update_info.account_balance += decimal.Decimal(float(balance_change))
        return db_access_object.update_table_record(account_update_info)

    def delete_account_by_id(self, account_id: int) -> bool:
        return db_access_object.delete_table_record(account_id, self.table_name)

    def transfer_to_account(self, from_account: Account, to_account: Account, amount_to_transfer: float) -> []:
        from_account.account_balance -= decimal.Decimal(float(amount_to_transfer))
        to_account.account_balance += decimal.Decimal(float(amount_to_transfer))
        accounts_list = [from_account, to_account]
        return db_access_object.update_multiple_related_records(accounts_list)
