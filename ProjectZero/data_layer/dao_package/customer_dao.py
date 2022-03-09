"""this module contains data access for customer object"""
from custom_exceptions.record_not_found import RecordNotFound
from data_entities.customer import Customer
from data_layer.dao_package.customer_dao_interface import CustomerDaoInterface
from data_layer.dao_package.db_access_for_data_layer import create_table_row_entry, \
    select_table_record, update_table_record, delete_table_record


class CustomerDao(CustomerDaoInterface):
    customer_unique_id = 1
    customer_list = []

    def __init__(self):
        # test customer for tests only in list data object version
        default_test_customer = Customer(0, "First", "Last")
        self.customer_id = default_test_customer.customer_id
        self.first_name = default_test_customer.first_name
        self.last_name = default_test_customer.last_name
        # used to identify which table will be accessed
        self.class_name = "customers"

    def create_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        #sql_query = "insert into customers values (default, %s, %s) returning customer_id"
        #cursor = connection.cursor()
        #cursor.execute(sql_query, (first_name, last_name))
        #connection.commit()
        #new_customer_id = cursor.fetchone()[0]
        #new_customer = self.get_customer_by_id(new_customer_id)
        #return new_customer
        customer_to_create = Customer(self.customer_unique_id, first_name, last_name)
        return create_table_row_entry(customer_to_create)
        #self.customer_unique_id += 1
        #self.customer_list.append(customer_to_create)
        #return customer_to_create

    def get_customer_by_id(self, get_customer_id: int) -> Customer:
        #sql_query = "select * from customers where customer_id = %s"
        #cursor = connection.cursor()
        #cursor.execute(sql_query, [customer_id])
        #connection.commit()
        #result_customer_tuple = cursor.fetchone()
        #customer_object = Customer(*result_customer_tuple)
        #return customer_object
        return select_table_record(get_customer_id, self.class_name)
        #for customers in self.customer_list:
        #    if customers.customer_id == customer_id:
        #        return customers
        #raise RecordNotFound("Customer record not found.")

    def update_customer(self, customer_id: int, first_name: str, last_name: str) -> Customer:
        customer_to_update = Customer(customer_id, first_name, last_name)
        return update_table_record(customer_to_update)
        #for customers in self.customer_list:
        #    if customers.customer_id == customer_id:
        #        customers.first_name = first_name
        #        customers.last_name = last_name
        #        return customers
        #raise RecordNotFound("Customer record not found.")

    def delete_customer_by_id(self, customer_id: int) -> bool:
        return delete_table_record(customer_id, self.class_name)
        #for customers in self.customer_list:
        #    if customers.customer_id == customer_id:
        #        self.customer_list.remove(customers)
        #        return True
        #return False


#test_object = CustomerDao()
#print(test_object.create_customer(0, "test", "name").__dict__)
