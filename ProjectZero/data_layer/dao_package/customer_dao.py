"""this module contains data access for customer object"""
from data_entities.customer import Customer
from data_layer.dao_package.customer_dao_interface import CustomerDaoInterface
from data_layer.dao_package.db_access_for_data_layer import DBAccessObject

db_access_object = DBAccessObject()


class CustomerDao(CustomerDaoInterface):
    customer_unique_id = 1
    customer_list = []

    def __init__(self):
        # used to identify which table will be accessed
        self.table_name = "customers"

    def create_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        customer_to_create = Customer(self.customer_unique_id, first_name, last_name)
        return db_access_object.create_table_row_entry(customer_to_create)

    def get_customer_by_id(self, get_customer_id: int) -> Customer:
        return db_access_object.select_table_record(get_customer_id, self.table_name)

    def update_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        customer_to_update = Customer(customer_id, first_name, last_name)
        return db_access_object.update_table_record(customer_to_update)

    def delete_customer_by_id(self, customer_id: int) -> bool:
        return db_access_object.delete_table_record(customer_id, self.table_name)
