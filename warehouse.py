from abc import ABC, abstractmethod

class StorageUnit(ABC):
    def __init__(self, unit_id, location, capacity):
        self.__unit_id = unit_id  # Encapsulated
        self.location = location
        self.capacity = capacity
        self.inventory = {}

    def get_unit_id(self):
        return self.__unit_id

    @abstractmethod
    def check_inventory(self):
        pass

    def store_product(self, product_id, quantity=1):  # Overload via default param
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        total_quantity = sum(self.inventory.values())
        if total_quantity + quantity > self.capacity:
            raise Exception("Not enough space in the storage unit.")
        self.inventory[product_id] = self.inventory.get(product_id, 0) + quantity

    def retrieve_product(self, product_id, quantity=1):
        if product_id not in self.inventory:
            raise Exception("Product not found.")
        if quantity > self.inventory[product_id]:
            raise Exception("Not enough stock.")
        self.inventory[product_id] -= quantity
        if self.inventory[product_id] == 0:
            del self.inventory[product_id]


class Warehouse(StorageUnit):
    def __init__(self, warehouse_id, location, capacity, manager_name=None):
        super().__init__(warehouse_id, location, capacity)
        self._manager_name = manager_name

    def store_product(self, product_id, quantity=1):  # Override
        try:
            super().store_product(product_id, quantity)
            print(f"Stored {quantity} units of product {product_id} in the warehouse.")
        except Exception as e:
            print(f"Error while storing product: {e}")

    def retrieve_product(self, product_id, quantity=1):  # Override
        try:
            super().retrieve_product(product_id, quantity)
            print(f"Retrieved {quantity} units of product {product_id} from the warehouse.")
        except Exception as e:
            print(f"Error while retrieving product: {e}")

    def check_inventory(self):  # Implement abstract method
        if not self.inventory:
            print("Warehouse inventory is empty.")
        else:
            print("Current warehouse inventory:")
            for product_id, quantity in self.inventory.items():
                print(f" - Product {product_id}: {quantity} units")

    def get_warehouse_info(self):
        print(f"Warehouse ID: {self.get_unit_id()}")
        print(f"Location: {self.location}")
        print(f"Capacity: {self.capacity}")
        print(f"Manager: {self._manager_name}")
        self.check_inventory()
