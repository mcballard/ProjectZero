"""this module will have the account data object"""

# accounts will have a unique account id
# accounts will have a bank id associated with the bank
# accounts will have a customer id associated with the owner of the account
# accounts will have a number that specifies the type checking, savings, business
# accounts will have a nonzero balance


class Account:
    def __init__(self, account_id: int, customer_id: int, account_balance: float):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_balance = account_balance
        self.class_name = "accounts"

    def __str__(self):
        return f"customer_id = {self.account_id}, first_name = {self.customer_id}, last_name = {self.account_balance}"

    def convert_to_dictionary_json_friendly(self):
        return {
            "accountId": self.account_id,
            "customerId": self.customer_id,
            "accountBalance": float(self.account_balance)
        }
