"""this module contains data access for customer object"""
from custom_exceptions.record_not_found import RecordNotFound
from data_entities.customer import Customer
from data_layer.dao_package.customer_dao_interface import CustomerDaoInterface


class CustomerDao(CustomerDaoInterface):
    customer_unique_id = 1
    customer_list = []

    def __init__(self):
        default_test_customer = Customer(0, "First", "Last")
        self.customer_id = default_test_customer.customer_id
        self.first_name = default_test_customer.first_name
        self.last_name = default_test_customer.last_name

    def create_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        customer_to_create = Customer(self.customer_unique_id, first_name, last_name)
        self.customer_unique_id += 1
        self.customer_list.append(customer_to_create)
        return customer_to_create

    def get_customer_by_id(self, customer_id: int) -> Customer:
        for customers in self.customer_list:
            if customers.customer_id == customer_id:
                return customers
        raise RecordNotFound("Customer record not found.")

    def update_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        for customers in self.customer_list:
            if customers.customer_id == customer_id:
                customers.first_name = first_name
                customers.last_name = last_name
                return customers
        raise RecordNotFound("Customer record not found.")

    def delete_customer_by_id(self, customer_id: int) -> bool:
        for customers in self.customer_list:
            if customers.customer_id == customer_id:
                self.customer_list.pop()
                return True
        return False
