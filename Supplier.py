from abc import ABC, abstractmethod

class Supplier(ABC):
    def __init__(self, supplier_id, name, contact_info, products_supplied, rating):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_info = contact_info
        self.products_supplied = products_supplied
        self.rating = rating

    @abstractmethod
    def supply_product(self):
        pass

    def get_supplier_info(self):
        return (
            f"Supplier ID: {self.supplier_id}\n"
            f"Name: {self.name}\n"
            f"Contact Info: {self.contact_info}\n"
            f"Products Supplied: {self.products_supplied}\n"
            f"Rating: {self.rating}/5"
        )

# Local parts supplier class
class LocalPartsSupplier(Supplier):
    def __init__(self, supplier_id, name, contact, location, part_type):
        super().__init__(supplier_id, name, contact, location)
        self.part_type = part_type

    def supply(self):
        return f"{self.name} supplies local {self.part_type} parts from {self.location}."

# International parts supplier class
class InternationalPartsSupplier(Supplier):
    def __init__(self, supplier_id, name, contact, location, country, part_type):
        super().__init__(supplier_id, name, contact, location)
        self.country = country
        self.part_type = part_type

    def supply(self):
        return f"{self.name} supplies international {self.part_type} parts from {self.country}."

# Battery supplier class
class BatterySupplier(Supplier):
    def __init__(self, supplier_id, name, contact, location, battery_type):
        super().__init__(supplier_id, name, contact, location)
        self.battery_type = battery_type

    def supply(self):
        return f"{self.name} supplies {self.battery_type} batteries from {self.location}."

# Supplier management class
class SupplierManager:
    def __init__(self):
        self.suppliers = []
        self.next_id = 1

    def add_supplier(self, name, contact, location):
        supplier = Supplier(self.next_id, name, contact, location)
        self.suppliers.append(supplier)
        self.next_id += 1

    def update_supplier(self, supplier_id, name=None, contact=None, location=None):
        supplier = self.find_supplier(supplier_id)
        if supplier:
            supplier.update_info(name, contact, location)

    def delete_supplier(self, supplier_id):
        supplier = self.find_supplier(supplier_id)
        if supplier:
            self.suppliers.remove(supplier)

    def find_supplier(self, supplier_id):
        for supplier in self.suppliers:
            if supplier.supplier_id == supplier_id:
                return supplier
        return None

# Order management class
class Order:
    def __init__(self, order_id, supplier, quantity, part_name):
        self.order_id = order_id
        self.supplier = supplier
        self.quantity = quantity
        self.part_name = part_name

    def get_order_details(self):
        return f"Order {self.order_id}: {self.quantity} units of {self.part_name} from {self.supplier.name}."

# Shipment management class
class Shipment:
    def __init__(self, shipment_id, order, delivery_date):
        self.shipment_id = shipment_id
        self.order = order
        self.delivery_date = delivery_date

    def get_shipment_details(self):
        return f"Shipment {self.shipment_id}: {self.order.get_order_details()} | Delivery on {self.delivery_date}."
