from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Union


class Location:
    """Standardized location class for addresses"""

    def __init__(self, address: str, city: str, country: str, postal_code: str):
        self.address = address
        self.city = city
        self.country = country
        self.postal_code = postal_code

    def __str__(self):
        return f"{self.address}, {self.city}, {self.country} {self.postal_code}"


class Product:
    """Product class with enhanced validation"""

    def __init__(self, product_id: str, name: str, category: str, price: float,
                 quantity: int, manufacture_date: date, warranty_years: int, expiry_date: Optional[date] = None):
        if price <= 0:
            raise ValueError("Price must be positive")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self._quantity = quantity
        self.manufacture_date = manufacture_date
        self.warranty_years = warranty_years
        self.expiry_date = expiry_date

    @property
    def quantity(self):
        return self._quantity

    def update_quantity(self, amount: int):
        if not isinstance(amount, int):
            raise ValueError("Amount must be an integer")
        if self._quantity + amount < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity += amount

    def get_info(self) -> Dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self._quantity,
            "manufacture_date": self.manufacture_date.strftime("%Y-%m-%d"),
            "warranty_years": self.warranty_years,
            "expiry_date": self.expiry_date.strftime("%Y-%m-%d") if self.expiry_date else None
        }

    def is_expired(self, check_date: date = None) -> bool:
        check_date = check_date or date.today()
        return self.expiry_date is not None and check_date > self.expiry_date


class Supplier(ABC):
    """Abstract base supplier class"""

    def __init__(self, supplier_id: str, name: str, contact_info: str,
                 products_supplied: List[str], rating: float, location: Location):
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5")

        self.supplier_id = supplier_id
        self.name = name
        self.contact_info = contact_info
        self.products_supplied = products_supplied
        self.rating = rating
        self.location = location

    @abstractmethod
    def supply_product(self, product: Product, quantity: int) -> bool:
        pass

    def get_info(self) -> Dict:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_info": self.contact_info,
            "products_supplied": self.products_supplied,
            "rating": self.rating,
            "location": str(self.location)
        }

    def update_info(self, name=None, contact_info=None, products_supplied=None, rating=None):
        if name:
            self.name = name
        if contact_info:
            self.contact_info = contact_info
        if products_supplied:
            self.products_supplied = products_supplied
        if rating:
            self.rating = rating



class LocalPartsSupplier(Supplier):
    def __init__(self, supplier_id: str, name: str, contact_info: str,
                 location: Location, part_type: str, rating: float = 5):
        products_supplied = [f"Local {part_type} parts"]
        super().__init__(supplier_id, name, contact_info, products_supplied, rating, location)
        self.part_type = part_type

    def supply_product(self, product: Product, quantity: int) -> bool:
        print(f"{self.name} supplied {quantity} {self.part_type} parts locally")
        return True


class InternationalPartsSupplier(Supplier):
    def __init__(self, supplier_id: str, name: str, contact_info: str,
                 location: Location, part_type: str, shipping_time_days: int, rating: float = 4):
        products_supplied = [f"International {part_type} parts"]
        super().__init__(supplier_id, name, contact_info, products_supplied, rating, location)
        self.part_type = part_type
        self.shipping_time_days = shipping_time_days

    def supply_product(self, product: Product, quantity: int) -> bool:
        print(f"{self.name} supplied {quantity} {self.part_type} parts internationally")
        return True


class BatterySupplier(Supplier):
    def __init__(self, supplier_id: str, name: str, contact_info: str,
                 location: Location, battery_type: str, rating: float = 4):
        products_supplied = [f"{battery_type} batteries"]
        super().__init__(supplier_id, name, contact_info, products_supplied, rating, location)
        self.battery_type = battery_type

    def supply_product(self, product: Product, quantity: int) -> bool:
        print(f"{self.name} supplied {quantity} {self.battery_type} batteries")
        return True


class SupplierManager:
    def __init__(self):
        self.suppliers: Dict[str, Supplier] = {}
        self.next_id = 1

    def add_supplier(self, supplier: Supplier) -> str:
        if not isinstance(supplier, Supplier):
            raise TypeError("Only Supplier instances can be added")

        supplier.supplier_id = f"SUP{self.next_id:04d}"
        self.suppliers[supplier.supplier_id] = supplier
        self.next_id += 1
        return supplier.supplier_id

    def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        return self.suppliers.get(supplier_id)

    def remove_supplier(self, supplier_id: str) -> bool:
        return self.suppliers.pop(supplier_id, None) is not None

    def list_suppliers(self) -> List[Dict]:
        return [supplier.get_info() for supplier in self.suppliers.values()]


class Manufacturer:
    def __init__(self, manufacturer_id: str, name: str, location: Location, production_capacity: int):
        self.manufacturer_id = manufacturer_id
        self.name = name
        self.location = location
        self.production_capacity = production_capacity
        self.products_produced: List[Product] = []
        self.raw_materials: List[Product] = []

    def add_raw_material(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Only Product instances can be added as raw materials")
        self.raw_materials.append(product)

    def manufacture_product(self, name: str, category: str, price: float,
                            quantity: int = 1, warranty_years: int = 1, expiry_days: Optional[int] = None) -> Optional[
        Product]:
        if len(self.products_produced) >= self.production_capacity:
            print("Production capacity reached!")
            return None

        manufacture_date = date.today()
        expiry_date = manufacture_date + timedelta(days=expiry_days) if expiry_days else None

        product_id = f"{name[:3].upper()}{len(self.products_produced) + 1:04d}"
        new_product = Product(
            product_id=product_id,
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            manufacture_date=manufacture_date,
            warranty_years=warranty_years,
            expiry_date=expiry_date
        )

        self.products_produced.append(new_product)
        return new_product

    def get_info(self) -> Dict:
        return {
            "manufacturer_id": self.manufacturer_id,
            "name": self.name,
            "location": str(self.location),
            "production_capacity": self.production_capacity,
            "products_produced": [p.get_info() for p in self.products_produced],
            "raw_materials": [rm.get_info() for rm in self.raw_materials]
        }


class Maintenance:
    def __init__(self, maintenance_id: str, product: Product, service_date: date,
                 service_type: str, service_details: str, cost: float, parts_replaced: List[str] = None):
        self.maintenance_id = maintenance_id
        self.product = product
        self.service_date = service_date
        self.service_type = service_type
        self.service_details = service_details
        self.cost = cost
        self.parts_replaced = parts_replaced if parts_replaced else []

    def get_info(self) -> Dict:
        return {
            "maintenance_id": self.maintenance_id,
            "product": self.product.get_info(),
            "service_date": self.service_date.strftime("%Y-%m-%d"),
            "service_type": self.service_type,
            "service_details": self.service_details,
            "cost": self.cost,
            "parts_replaced": self.parts_replaced
        }

    def __str__(self):
        return f"[{self.service_date}] {self.product.name} - {self.service_type}: ${self.cost:.2f}"





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
    def __init__(self, warehouse, today_date=None):
        self.warehouse = warehouse
        self.today_date = today_date or date.today()

    def is_inventory_full(self):
        total_quantity = sum(self.warehouse.inventory.values()) if isinstance(next(iter(self.warehouse.inventory.values()), None), int) else sum(item['quantity'] for item in self.warehouse.inventory.values())
        return total_quantity >= self.warehouse.capacity

    def remove_expired_if_full(self):
        if not self.is_inventory_full():
            print("Inventory is not full. No expired items removed.")
            return

        removed = False
        for product_id in list(self.warehouse.inventory.keys()):
            item = self.warehouse.inventory[product_id]
            if isinstance(item, dict) and 'expiry' in item and item['expiry'] < self.today_date:
                del self.warehouse.inventory[product_id]
                print(f"Removed expired product: {product_id}")
                removed = True

        if not removed:
            print("No expired products found.")




class Distributor:
    def __init__(self, distributor_id: str, name: str, location: Location):
        self.distributor_id = distributor_id
        self.name = name
        self.location = location
        self.inventory: List[Product] = []
        self.orders_processed: List['Order'] = []

    def add_to_inventory(self, product: Product) -> bool:
        if not isinstance(product, Product):
            raise TypeError("Only Product instances can be added to inventory")
        self.inventory.append(product)
        return True

    def distribute_product(self, retailer: 'Retailer', product: Product, quantity: int) -> bool:
        available = sum(1 for p in self.inventory if p.product_id == product.product_id)
        if available < quantity:
            return False

        distributed = 0
        for _ in range(quantity):
            for i, p in enumerate(self.inventory):
                if p.product_id == product.product_id:
                    retailer.receive_product(self.inventory.pop(i))
                    distributed += 1
                    break

        return distributed == quantity

    def get_info(self) -> Dict:
        return {
            "distributor_id": self.distributor_id,
            "name": self.name,
            "location": str(self.location),
            "inventory_count": len(self.inventory),
            "orders_processed": len(self.orders_processed)
        }


class Order:
    def __init__(self, order_id: str, product: Product, quantity: int, price_per_unit: float):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.order_date = date.today()
        self.status = "Pending"  # Pending, Processing, Shipped, Delivered, Cancelled
        self.estimated_delivery = self.calculate_delivery_date()

    def calculate_delivery_date(self) -> date:
        if self.product.category == "Engine":
            return self.order_date + timedelta(days=7)
        elif self.product.category == "Battery":
            return self.order_date + timedelta(days=5)
        else:
            return self.order_date + timedelta(days=10)

    def update_status(self, new_status: str) -> bool:
        valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
        if new_status not in valid_statuses:
            return False
        self.status = new_status
        return True

    def get_info(self) -> Dict:
        return {
            "order_id": self.order_id,
            "product": self.product.get_info(),
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "total_price": self.quantity * self.price_per_unit,
            "order_date": self.order_date.strftime("%Y-%m-%d"),
            "status": self.status,
            "estimated_delivery": self.estimated_delivery.strftime("%Y-%m-%d")
        }


class Marketing:
    def __init__(self, strategy: str, budget: float):
        self.strategy = strategy
        self.budget = budget
        self.campaigns: List[Dict] = []
        self.reach = 0

    def run_campaign(self, campaign_name: str, duration_days: int) -> bool:
        multipliers = {
            "Social Media": 75,
            "TV Ads": 120,
            "Billboards": 50,
            "Email Marketing": 40
        }

        multiplier = multipliers.get(self.strategy, 60)
        self.reach = int(self.budget * multiplier)

        campaign = {
            "name": campaign_name,
            "strategy": self.strategy,
            "budget": self.budget,
            "duration": duration_days,
            "reach": self.reach,
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=duration_days)
        }

        self.campaigns.append(campaign)
        return True

    def analyze_market(self) -> str:
        if self.reach > 100000:
            return "High Demand"
        elif self.reach > 50000:
            return "Stable Market"
        else:
            return "Low Interest"

    def get_info(self) -> Dict:
        return {
            "strategy": self.strategy,
            "budget": self.budget,
            "total_reach": self.reach,
            "campaigns": self.campaigns,
            "market_analysis": self.analyze_market()
        }


class Store(ABC):
    def __init__(self, store_id: str, name: str, location: Location):
        self.store_id = store_id
        self.name = name
        self.location = location
        self.inventory: List[Product] = []

    def add_product(self, product: Product) -> bool:
        if not isinstance(product, Product):
            raise TypeError("Only Product instances can be added")
        self.inventory.append(product)
        return True

    def sell_product(self, product_id: str) -> Optional[Product]:
        for i, product in enumerate(self.inventory):
            if product.product_id == product_id:
                return self.inventory.pop(i)
        return None

    def get_info(self) -> Dict:
        return {
            "store_id": self.store_id,
            "name": self.name,
            "location": str(self.location),
            "inventory_count": len(self.inventory),
            "inventory_value": sum(p.price for p in self.inventory)
        }


class Retailer(Store):
    def __init__(self, retailer_id: str, name: str, location: Location):
        super().__init__(retailer_id, name, location)
        self.orders: List[Order] = []

    def place_order(self, distributor: Distributor, product: Product, quantity: int) -> Optional[Order]:
        order_id = f"ORD-{len(self.orders) + 1:06d}"
        order = Order(order_id, product, quantity, product.price)
        self.orders.append(order)

        if distributor.distribute_product(self, product, quantity):
            order.update_status("Shipped")
            return order
        else:
            order.update_status("Cancelled")
            return None

    def receive_product(self, product: Product) -> bool:
        return self.add_product(product)

    def get_info(self) -> Dict:
        base_info = super().get_info()
        base_info.update({
            "type": "Retailer",
            "orders_placed": len(self.orders),
            "active_orders": sum(1 for o in self.orders if o.status != "Delivered")
        })
        return base_info


class CarStore(Store):
    def __init__(self, store_id: str, name: str, location: Location, brand: str):
        super().__init__(store_id, name, location)
        self.brand = brand
        self.test_drives = 0

    def arrange_test_drive(self) -> bool:
        if len(self.inventory) == 0:
            return False
        self.test_drives += 1
        return True

    def get_info(self) -> Dict:
        base_info = super().get_info()
        base_info.update({
            "type": "CarStore",
            "brand": self.brand,
            "test_drives": self.test_drives
        })
        return base_info


class SupplyChain:
    """Main coordination class for the entire supply chain"""

    def __init__(self):
        self.suppliers = SupplierManager()
        self.manufacturers: Dict[str, Manufacturer] = {}
        self.distributors: Dict[str, Distributor] = {}
        self.retailers: Dict[str, Retailer] = {}
        self.stores: Dict[str, Store] = {}
        self.warehouses: Dict[str, Warehouse] = {}
        self.products: Dict[str, Product] = {}

    def add_manufacturer(self, name: str, location: Location, capacity: int) -> str:
        manufacturer_id = f"MAN{len(self.manufacturers) + 1:04d}"
        self.manufacturers[manufacturer_id] = Manufacturer(manufacturer_id, name, location, capacity)
        return manufacturer_id

    def add_distributor(self, name: str, location: Location) -> str:
        distributor_id = f"DIST{len(self.distributors) + 1:04d}"
        self.distributors[distributor_id] = Distributor(distributor_id, name, location)
        return distributor_id

    def add_retailer(self, name: str, location: Location) -> str:
        retailer_id = f"RET{len(self.retailers) + 1:04d}"
        self.retailers[retailer_id] = Retailer(retailer_id, name, location)
        return retailer_id

    def add_car_store(self, name: str, location: Location, brand: str) -> str:
        store_id = f"CAR{len(self.stores) + 1:04d}"
        self.stores[store_id] = CarStore(store_id, name, location, brand)
        return store_id

    def add_warehouse(self, location: Location, capacity: int, manager: str = None) -> str:
        warehouse_id = f"WH{len(self.warehouses) + 1:04d}"
        self.warehouses[warehouse_id] = Warehouse(warehouse_id, location, capacity, manager)
        return warehouse_id

    def get_supply_chain_status(self) -> Dict:
        return {
            "suppliers": len(self.suppliers.list_suppliers()),
            "manufacturers": len(self.manufacturers),
            "distributors": len(self.distributors),
            "retailers": len(self.retailers),
            "stores": len(self.stores),
            "warehouses": len(self.warehouses),
            "products": len(self.products)
        }

