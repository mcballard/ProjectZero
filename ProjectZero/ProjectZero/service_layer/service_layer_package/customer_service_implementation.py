"""this module contains the implementation for customer interactions in the service layer"""
from custom_exceptions.incorrect_data_field import IncorrectDataField
from custom_exceptions.string_too_long import StringTooLong
from data_entities.customer import Customer
from data_layer.dao_package.customer_dao_interface import CustomerDaoInterface
from service_layer.service_layer_package.customer_service_interface import CustomerSlInterface


class CustomerSlImp(CustomerSlInterface):

    def __init__(self, customer_dao: CustomerDaoInterface):
        self.customer_dao = customer_dao

    def sl_create_customer(self, first_name: str, last_name: str) -> Customer:
        if (type(first_name) != str) or (type(last_name) != str):
            raise IncorrectDataField("The name value must be a string.")
        elif (len(first_name) > 20) or (len(last_name) > 20):
            raise StringTooLong("The name value must be a string less than 20 characters.")
        # 0 is used as placeholder value for customer id during customer creation
        return self.customer_dao.create_customer(0, first_name, last_name)

    def sl_update_customer_by_id(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        if (type(first_name) != str) or (type(last_name) != str):
            raise IncorrectDataField("The name value must be a string.")
        elif (len(first_name) > 20) or (len(last_name) > 20):
            raise StringTooLong("The name value must be a string less than 20 characters.")
        return self.customer_dao.update_customer(customer_id, first_name, last_name)

    def sl_get_customer_by_id(self, customer_id: int) -> Customer:
        if type(customer_id) != int:
            raise IncorrectDataField("The customer id must be an integer.")
        return self.customer_dao.get_customer_by_id(customer_id)

    def sl_delete_customer_by_id(self, customer_id: int) -> bool:
        if type(customer_id) != int:
            raise IncorrectDataField("The customer id must be an integer.")
        return self.customer_dao.delete_customer_by_id(customer_id)

