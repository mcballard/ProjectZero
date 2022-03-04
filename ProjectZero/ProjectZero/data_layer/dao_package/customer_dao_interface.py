"""this module contains the interface for the customer data access object"""

#  Data access should have create, read, update and delete


from abc import ABC, abstractmethod

from data_entities.customer import Customer


class CustomerDaoInterface(ABC):

    @abstractmethod
    def create_customer(self, customer_id: int, first_name: str, last_name: str)-> Customer:
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Customer:
        pass

    @abstractmethod
    def update_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        pass

    @abstractmethod
    def delete_customer_by_id(self, customer_id: int) -> bool:
        pass

