"""this module contains the implementation of the service level account interactions"""
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
            #  0 is used as placeholder for customer_id in creating new account
            raise IncorrectDataField("The account balance must be a number.")
        return self.account_dao.create_account(0, customer_id, account_balance)

    def sl_get_account_info_by_id(self, account_id: int) -> Account:
        return self.account_dao.get_account_info_by_id(account_id)

    def sl_get_all_accounts_by_customer_id(self, customer_id: int) -> []:
        return self.account_dao.get_all_accounts_by_customer_id(customer_id)

    def sl_update_account_by_id(self, account_id: int, balance_change: float) -> Account:
        pass  # this function isn't explicitly implemented on purpose

    def sl_delete_account_by_account_id(self, account_id: int) -> bool:
        for accounts in self.account_dao.account_list:
            if accounts.account_id == account_id:
                self.account_dao.account_list.remove(accounts)
                return True
        return False

    def sl_leave_bank_by_customer_id(self, customer_id: int) -> []:
        is_record_removed = False
        amount_withdrawn = 0
        accounts_to_close = self.sl_get_all_accounts_by_customer_id(customer_id)
        for accounts in accounts_to_close:
            amount_to_withdraw = accounts.account_balance
            closed_account = self.withdraw_from_account_by_id(accounts.account_id, amount_to_withdraw)
            amount_withdrawn += amount_to_withdraw
            is_record_removed = self.sl_delete_account_by_account_id(closed_account.account_id)
        if is_record_removed and (amount_withdrawn != 0):
            return True, amount_withdrawn
        else:
            raise RecordNotFound("No accounts closed.")

    def sl_close_account_by_id(self, account_id: int) -> []:
        is_record_removed = False
        account_to_close = self.sl_get_account_info_by_id(account_id)
        amount_to_withdraw = account_to_close.account_balance
        closed_account = self.withdraw_from_account_by_id(account_to_close.account_id, amount_to_withdraw)
        for accounts in self.account_dao.account_list:
            if accounts.account_id == account_id:
                self.account_dao.account_list.remove(accounts)
                is_record_removed = True
                break
        if is_record_removed and (closed_account.account_balance == 0):
            return True, amount_to_withdraw
        else:
            return False

    def deposit_to_account_by_id(self, account_id: int, amount_to_change: float) -> Account:
        for accounts in self.account_dao.account_list:
            if accounts.account_id == account_id:
                account_to_change = self.account_dao.get_account_info_by_id(account_id)
                updated_account = self.account_dao.update_account_by_id(account_to_change.account_id, amount_to_change)
                return updated_account
        raise RecordNotFound("Account not found.")

    def withdraw_from_account_by_id(self, account_id: int, amount_to_change: float) -> Account:
        for accounts in self.account_dao.account_list:
            if accounts.account_id == account_id:
                if accounts.account_balance < amount_to_change:
                    raise NegativeBalance("You do not have sufficient funds.")
                else:
                    account_to_change = self.account_dao.get_account_info_by_id(account_id)
                    updated_account = self.account_dao.update_account_by_id(account_to_change.account_id, -amount_to_change)
                    return updated_account
        raise RecordNotFound("Account not found.")

    def transfer_to_account(self, from_account: Account, to_account: Account, amount_to_transfer: float) -> []:
        if from_account.account_balance < amount_to_transfer:
            raise NegativeBalance("You cannot overdraw your account.")
        else:
            for existing_account in self.account_dao.account_list:
                if from_account.account_id == existing_account.account_id:
                    account_to_withdraw = self.sl_get_account_info_by_id(from_account.account_id)
                    withdrawn_account = self.withdraw_from_account_by_id(account_to_withdraw.account_id, amount_to_transfer)
                elif to_account.account_id == existing_account.account_id:
                    account_to_transfer = self.sl_get_account_info_by_id(to_account.account_id)
                    deposited_account = self.deposit_to_account_by_id(account_to_transfer.account_id, amount_to_transfer)
        return withdrawn_account, deposited_account
