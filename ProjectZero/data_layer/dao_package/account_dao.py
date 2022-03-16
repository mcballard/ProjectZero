"""this module contains data access for account object"""
from custom_exceptions.negative_balance import NegativeBalance
from data_entities.account import Account
from data_layer.dao_package.account_DAO_interface import AccountDaoInterface
from data_layer.dao_package.db_access_for_data_layer import create_table_row_entry, \
    select_table_record, select_all_table_records_by_id, update_table_record, delete_table_record, \
    update_multiple_related_records


class AccountDao(AccountDaoInterface):

    def __init__(self):
        self.class_name = "accounts"

    def create_account(self, account_id: int, customer_id: int, account_balance: float) -> Account:
        if account_balance < 0:
            raise NegativeBalance("Cannot have negative account balance.")
        else:
            account_to_create = Account(account_id, customer_id, account_balance)
            return create_table_row_entry(account_to_create)

    def get_account_info_by_id(self, account_id: int) -> Account:
        return select_table_record(account_id, self.class_name)

    def get_all_accounts_by_customer_id(self, customer_id: int) -> []:
        customer_to_get_accounts_for = Account(0, customer_id, 0)
        return select_all_table_records_by_id(customer_to_get_accounts_for)

    def update_account_by_id(self, account_id: int, balance_change: float) -> Account:
        account_update_info: Account = select_table_record(account_id, self.class_name)
        account_update_info.account_balance += balance_change
        return update_table_record(account_update_info)

    def delete_account_by_id(self, account_id: int) -> bool:
        return delete_table_record(account_id, self.class_name)

    def transfer_to_account(self, from_account: Account, to_account: Account, amount_to_transfer: float) -> []:
        from_account.account_balance -= amount_to_transfer
        to_account.account_balance += amount_to_transfer
        return update_multiple_related_records(from_account, to_account)
