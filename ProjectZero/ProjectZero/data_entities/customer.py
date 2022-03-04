"""this module contains customer data object"""

# the customer will have a unique id
# the customer will have a name, first and last 2 string fields must not exceed 20 characters each
# the customer will have an account or multiple accounts business, checking, savings identified by numbers if they do
#   have a particular type of account the number will have a default value


class Customer:
    def __init__(self, customer_id: int, first_name: str, last_name: str):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
