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
        self.class_name = "customers"

    def __str__(self):
        return f"customer_id = {self.customer_id}, first_name = {self.first_name}, last_name = {self.last_name}"

    def convert_to_dictionary_json_friendly(self):
        return {
            "customerID": self.customer_id,
            "firstName": self.first_name,
            "lastName": self.last_name
        }
