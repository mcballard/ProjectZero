"""this module contains service layer interface"""
from abc import ABC, abstractmethod
from data_entities.customer import Customer


class CustomerSlInterface(ABC):

    @abstractmethod
    def sl_create_customer(self, first_name: str, last_name: str) -> Customer:
        pass  # this method should sanitize the input to the data layer for the create functions

    @abstractmethod
    def sl_update_customer_by_id(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        pass

    @abstractmethod
    def sl_get_customer_by_id(self, customer_id: int) -> Customer:
        pass

    @abstractmethod
    def sl_delete_customer_by_id(self, customer_id: int) -> bool:
        pass
