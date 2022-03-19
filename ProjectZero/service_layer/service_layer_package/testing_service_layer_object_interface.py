from abc import ABC, abstractmethod

from data_entities.testing_implemented_table_object import TestRowObject


class TestServiceLayerObjectInterface(ABC):

    @abstractmethod
    def sanitize_json_from_api(self, json_from_api: dict) -> dict:
        pass

    @abstractmethod
    def create_record_business_logic_data_manipulation(self, row_object_from_api: TestRowObject) -> dict:
        pass

    @abstractmethod
    def select_record_business_logic_data_manipulation(self, row_object_id: int) -> dict:
        pass

    @abstractmethod
    def update_record_business_logic_data_manipulation(self, row_object_from_api: TestRowObject) -> dict:
        pass

    @abstractmethod
    def delete_record_business_logic_data_manipulation(self, row_object_id: int) -> bool:
        pass
