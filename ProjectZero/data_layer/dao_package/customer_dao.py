"""this module contains data access for customer object"""
from data_entities.customer import Customer
from data_layer.dao_package.customer_dao_interface import CustomerDaoInterface
from data_layer.dao_package.db_access_for_data_layer import create_table_row_entry, \
    select_table_record, update_table_record, delete_table_record


class CustomerDao(CustomerDaoInterface):
    customer_unique_id = 1
    customer_list = []

    def __init__(self):
        # used to identify which table will be accessed
        self.class_name = "customers"

    def create_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        customer_to_create = Customer(self.customer_unique_id, first_name, last_name)
        return create_table_row_entry(customer_to_create)

    def get_customer_by_id(self, get_customer_id: int) -> Customer:
        return select_table_record(get_customer_id, self.class_name)

    def update_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        customer_to_update = Customer(customer_id, first_name, last_name)
        return update_table_record(customer_to_update)

    def delete_customer_by_id(self, customer_id: int) -> bool:
        return delete_table_record(customer_id, self.class_name)
