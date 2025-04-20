from abc import ABC, abstractmethod

class StorageUnit(ABC):
    def __init__(self, unit_id, location, capacity):
        self.__unit_id = unit_id  
        self.location = location
        self.capacity = capacity
        self.inventory = {}

    def get_unit_id(self):
        return self.__unit_id

    @abstractmethod
    def check_inventory(self):
        pass

    def store_product(self, product_id, quantity=1):  # Overide
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

    def check_inventory(self):  # abstract method
        if not self.inventory:
            print("Warehouse inventory is empty.")
        else:
            print("Current warehouse inventory:")
            for product_id, quantity in self.inventory.items():
                print(f"Product {product_id}: {quantity} units")

    def get_warehouse_info(self):
        print(f"Warehouse ID: {self.get_unit_id()}")
        print(f"Location: {self.location}")
        print(f"Capacity: {self.capacity}")
        print(f"Manager: {self._manager_name}")
        self.check_inventory()


class ExpiryManager:
    def __init__(self, warehouse):
        self.warehouse = warehouse

    def is_inventory_full(self):
        total_quantity = sum([item['quantity'] for item in self.warehouse.inventory.values()])
        return total_quantity >= self.warehouse.capacity

    def remove_expired_if_full(self):
        if not self.is_inventory_full():
            print("Inventory is not full. No expired items removed.")
            return

    def remove_expired_if_full(self):
        if not self.is_inventory_full():
            print("Inventory is not full. No expired items removed.")
            return

        removed = False
        for product_id in list(self.warehouse.inventory.keys()):
            expiry = self.warehouse.inventory[product_id]['expiry']
            if expiry < self.today_date: 
                del self.warehouse.inventory[product_id]
                print(f"Removed expired product: {product_id}")
                removed = True

        if not removed:
            print("No expired products found.")
