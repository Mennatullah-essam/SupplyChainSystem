from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Union
from multipledispatch import dispatch
import sqlite3


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


class SupplierManagerProxy:
    def __init__(self, user_role: str):
        self.user_role = user_role
        self.manager = SupplierManager()

    def add_supplier(self, supplier: Supplier):
        if self.user_role == "admin":
            return self.manager.add_supplier(supplier)
        else:
            print("Access denied: Only admins can add suppliers.")

    def get_supplier(self, supplier_id: str):
        if self.user_role == "admin":
            return self.manager.get_supplier(supplier_id)
        else:
            print("Access denied: Only admins can view supplier details.")

    def remove_supplier(self, supplier_id: str):
        if self.user_role == "admin":
            return self.manager.remove_supplier(supplier_id)
        else:
            print("Access denied: Only admins can remove suppliers.")

    def list_suppliers(self):
        if self.user_role == "admin":
            return self.manager.list_suppliers()
        else:
            print("Access denied: Only admins can list suppliers.")


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

    @dispatch(str, int)
    def store_product(self, product_id, quantity=1):
        """Handle storage by product ID"""
        try:
            super().store_product(product_id, quantity)
            print(f"Stored {quantity} units of product {product_id} in the warehouse.")
        except Exception as e:
            print(f"Error while storing product: {e}")

    @dispatch(Product, int)
    def store_product(self, product, quantity=1):
        """Handle storage by Product instance"""
        self.store_product(product.product_id, quantity)

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
        if not self.warehouse.inventory:
            return False
        total_quantity = sum(self.warehouse.inventory.values()) if isinstance(next(iter(self.warehouse.inventory.values())), int) else sum(item['quantity'] for item in self.warehouse.inventory.values())
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
        self.status = "Pending"
        self.__payment_processor = PaymentProcessor()  # Singleton instance

    def update_status(self, new_status: str):
        """Update the order status"""
        valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        self.status = new_status

    def get_order_value(self) -> float:
        """Calculate total order value"""
        return self.quantity * self.price_per_unit

    def process_payment(self) -> bool:
        """Process payment using the Singleton payment processor"""
        total_amount = self.quantity * self.price_per_unit
        return self.__payment_processor.process(self.order_id, total_amount)


class PaymentProcessor:
    """Singleton payment processing system"""
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__transactions = {}
            cls._instance.__total_balance = 0.0
        return cls._instance

    def process(self, order_id: str, amount: float) -> bool:
        """Process a payment transaction"""
        if order_id in self.__transactions:
            return False  # Prevent duplicate payments
        
        # Simulate actual payment processing
        self.__transactions[order_id] = {
            'amount': amount,
            'timestamp': datetime.now(),
            'status': 'completed'
        }
        self.__total_balance += amount
        return True

    def get_total_balance(self) -> float:
        """Get cumulative balance of all processed payments"""
        return self.__total_balance

    def get_transaction_count(self) -> int:
        """Get total number of processed transactions"""
        return len(self.__transactions)


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


class User:
    current_user = None

    def __init__(self, id=None, username=None, name=None, role=None, email=None, password=None):
        self.id = id
        self.username = username
        self.name = name
        self.role = role
        self.email = email
        self.password = password

    @classmethod
    def get_connection(cls, db_name):
        try: 
            return sqlite3.connect(db_name)
        except Exception as e: 
            print(f"exception1 {e}")
            raise

    @classmethod
    def create_table(cls, connection):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT UNIQUE,
            password TEXT NOT NULL
        )
        """
        try:
            with connection:
                connection.execute(query)
            print("Table created")
        except Exception as e:
            print(f"exception2 {e}")

    @classmethod
    def register_user(cls, connection):
        print("\n--- Register New User ---")
        username = input("Enter username: ")

        existing = cls.fetch_users(connection, f"username = '{username}'")
        if existing:
            print("Username already exists!")
            return

        name = input("Enter full name: ")
        role = input("Enter role: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")

        if password != confirm_password:
            print("Passwords don't match!")
            return

        max_id = connection.execute("SELECT MAX(id) FROM users").fetchone()[0]
        new_id = 1 if max_id is None else max_id + 1

        query = "INSERT INTO users (id, username, name, role, email, password) VALUES (?, ?, ?, ?, ?, ?)"
        try: 
            with connection:
                connection.execute(query, (new_id, username, name, role, email, password))
                print(f"User {username} registered successfully!")
        except Exception as e:
            print(f"Registration failed: {e}")

    @classmethod
    def login(cls, connection):
        print("\n--- Login ---")
        username = input("Username: ")
        password = input("Password: ")

        user = cls.fetch_users(connection, f"username = '{username}' AND password = '{password}'")
        if user:
            cls.current_user = cls(*user[0])  # Create User instance
            print(f"Welcome {cls.current_user.name} ({cls.current_user.role})!")
            cls.current_user.do_role_action()
            return True
        else:
            print("Invalid username or password!")
            return False

    @classmethod
    def logout(cls):
        if cls.current_user:
            print(f"Goodbye {cls.current_user.name}!")
            cls.current_user = None
        else:
            print("No user is currently logged in.")

    def do_role_action(self):
        if self.role.lower() == 'admin':
            print("Doing admin tasks: managing users, configuring system...")
        elif self.role.lower() == 'manager':
            print("Doing manager tasks: overseeing operations, reporting...")
        elif self.role.lower() == 'user':
            print("Doing user tasks: regular work activities...")
        else:
            print(f"Doing {self.role} tasks: specialized work...")

    @classmethod
    def check_login(cls, required_role=None):
        if not cls.current_user:
            print("Please login first!")
            return False
        if required_role and cls.current_user.role != required_role:
            print(f"You need {required_role} privileges for this action!")
            return False
        return True

    @classmethod
    def insert_user(cls, connection, name: str, role: str, email: str):
        if not cls.check_login('admin'):
            return

        query = "INSERT INTO users (username, name, role, email, password) VALUES (?, ?, ?, ?, ?)"
        try: 
            username = email.split('@')[0]
            password = "default123"
            with connection:
                connection.execute(query, (username, name, role, email, password))
                print(f"User {name} was added")
        except Exception as e:
            print(f"exception3 {e}")

    @classmethod
    def fetch_users(cls, connection, condition: str = None):
        query = "SELECT * FROM users"
        if condition:
            query += f" WHERE {condition}"

        try:
            with connection:
                rows = connection.execute(query).fetchall()
            return rows    
        except Exception as e:
            print(f"exception 4 {e}")
            return []

    @classmethod
    def delete_user(cls, connection, id: int):
        if not cls.check_login('admin'):
            return

        query = "DELETE FROM users WHERE id = ?"
        try: 
            with connection:
                connection.execute(query, (id,))
            print(f"user: {id} deleted.")
        except Exception as e:
            print(f"exception 5 {e}")

    @classmethod
    def update_user(cls, connection, id, email):
        if not cls.check_login():
            return

        query = "UPDATE users SET email = ? WHERE id = ?"
        try: 
            with connection:
                connection.execute(query, (email, id))
            print("User email updated")
        except Exception as e:
            print(f"exception 6 {e}") 

    @classmethod
    def insert_many_users(cls, connection, users):
        if not cls.check_login('admin'):
            return

        query = "INSERT INTO users (username, name, role, email, password) VALUES (?, ?, ?, ?, ?)"
        try: 
            with connection:
                processed_users = []
                for name, role, email in users:
                    username = email.split('@')[0]
                    password = "default123"
                    processed_users.append((username, name, role, email, password))

                connection.executemany(query, processed_users)
            print(f"{len(users)} users were added")
        except Exception as e:
            print(f"exception 7 {e}")

    @classmethod
    def main(cls):
        connection = cls.get_connection("database3.db")
        cls.create_table(connection)

        while True:
            if cls.current_user:
                print(f"\nLogged in as {cls.current_user.name} ({cls.current_user.role})")
                print("1. Logout")
                print("2. Add User (Admin only)")
                print("3. Search Users")
                print("4. Update Email")
                print("5. Delete User (Admin only)")
                print("6. Add Multiple Users (Admin only)")
                print("7. Exit")
            else:
                print("\n1. Login")
                print("2. Register")
                print("3. Exit")

            choice = input("Enter your choice: ")

            if cls.current_user:
                if choice == "1":
                    cls.logout()
                elif choice == "2":
                    name = input("Enter name: ")
                    role = input("Enter role: ")
                    email = input("Enter email: ")
                    cls.insert_user(connection, name, role, email)
                elif choice == "3":
                    for user in cls.fetch_users(connection):
                        print(user)
                elif choice == "4":
                    id = int(input("Enter user ID to update: "))
                    email = input("Enter new email: ")
                    cls.update_user(connection, id, email)
                elif choice == "5":
                    id = int(input("Enter user ID to delete: "))
                    cls.delete_user(connection, id)
                elif choice == "6":
                    users = []
                    while True:
                        name = input("Enter name (or 'done' to finish): ")
                        if name.lower() == 'done':
                            break
                        role = input("Enter role: ")
                        email = input("Enter email: ")
                        users.append((name, role, email))
                    if users:
                        cls.insert_many_users(connection, users)
                elif choice == "7":
                    break
            else:
                if choice == "1":
                    cls.login(connection)
                elif choice == "2":
                    cls.register_user(connection)
                elif choice == "3":
                    break

        connection.close()


if __name__ == "__main__":
    # Create locations
    ny_location = Location("123 Main St", "New York", "USA", "10001")
    la_location = Location("456 Sunset Blvd", "Los Angeles", "USA", "90028")
    china_location = Location("789 Industrial Park", "Shanghai", "China", "200000")
    germany_location = Location("101 Autobahn Ave", "Munich", "Germany", "80333")
    texas_location = Location("202 Lone Star Rd", "Austin", "USA", "78701")

    # Create products
    today = date.today()
    next_year = today.replace(year=today.year + 1)

    battery = Product(
        product_id="BAT001",
        name="Lithium Battery",
        category="Energy",
        price=199.99,
        quantity=100,
        manufacture_date=today,
        warranty_years=2,
        expiry_date=next_year
    )

    engine = Product(
        product_id="ENG002",
        name="V8 Engine",
        category="Mechanical",
        price=4999.99,
        quantity=50,
        manufacture_date=today,
        warranty_years=5
    )

    tire = Product(
        product_id="TIR003",
        name="All-Season Tire",
        category="Wheels",
        price=149.99,
        quantity=200,
        manufacture_date=today,
        warranty_years=3
    )

    # Create suppliers
    supplier_manager = SupplierManager()

    local_supplier = LocalPartsSupplier(
        supplier_id="",
        name="NY Auto Parts",
        contact_info="contact@nyautoparts.com",
        location=ny_location,
        part_type="engine"
    )
    local_supplier_id = supplier_manager.add_supplier(local_supplier)

    international_supplier = InternationalPartsSupplier(
        supplier_id="",
        name="Shanghai Auto Parts",
        contact_info="contact@shanghaiauto.com",
        location=china_location,
        part_type="electronics",
        shipping_time_days=14
    )
    international_supplier_id = supplier_manager.add_supplier(international_supplier)

    battery_supplier = BatterySupplier(
        supplier_id="",
        name="Munich Battery Co",
        contact_info="sales@munichbattery.de",
        location=germany_location,
        battery_type="lithium-ion"
    )
    battery_supplier_id = supplier_manager.add_supplier(battery_supplier)

    # Create manufacturer
    auto_manufacturer = Manufacturer(
        manufacturer_id="MAN0001",
        name="Tesla Motors",
        location=la_location,
        production_capacity=1000
    )

    # Add raw materials to manufacturer
    auto_manufacturer.add_raw_material(battery)
    auto_manufacturer.add_raw_material(engine)

    # Manufacture a product
    electric_car = auto_manufacturer.manufacture_product(
        name="Model S",
        category="Electric Vehicle",
        price=79999.99,
        quantity=1,
        warranty_years=8,
        expiry_days=365*15  # 15 years
    )

    # Create warehouse
    main_warehouse = Warehouse(
        warehouse_id="WH001",
        location=texas_location,
        capacity=5000,
        manager_name="John Warehouse"
    )

    # Store products in warehouse
    main_warehouse.store_product(battery, 100)
    main_warehouse.store_product(engine, 50)
    main_warehouse.store_product(tire, 200)

    # Create distributor
    us_distributor = Distributor(
        distributor_id="DIST001",
        name="USA Auto Distributors",
        location=ny_location
    )

    # Add products to distributor inventory
    us_distributor.add_to_inventory(battery)
    us_distributor.add_to_inventory(engine)
    us_distributor.add_to_inventory(tire)

    # Create retailer
    auto_retailer = Retailer(
        retailer_id="RET001",
        name="Best Auto Sales",
        location=la_location
    )

    # Place order from retailer to distributor
    retailer_order = auto_retailer.place_order(
        distributor=us_distributor,
        product=battery,
        quantity=10
    )

    # Create car store
    premium_car_store = CarStore(
        store_id="CAR001",
        name="Luxury Auto Gallery",
        location=ny_location,
        brand="Tesla"
    )

    # Add products to car store
    premium_car_store.add_product(electric_car)

    # Arrange test drive
    premium_car_store.arrange_test_drive()

    # Create maintenance record
    car_maintenance = Maintenance(
        maintenance_id="MNT001",
        product=electric_car,
        service_date=today,
        service_type="Annual Checkup",
        service_details="Full vehicle inspection and software update",
        cost=199.99,
        parts_replaced=["Air Filter"]
    )

    # Create marketing campaign
    ev_marketing = Marketing(
        strategy="Social Media",
        budget=5000.00
    )
    ev_marketing.run_campaign(
        campaign_name="Electric Revolution",
        duration_days=30
    )

    # Create supply chain and add all components
    supply_chain = SupplyChain()
    supply_chain.suppliers = supplier_manager

    # Add manufacturer to supply chain
    supply_chain.add_manufacturer(
        name="Tesla Motors",
        location=la_location,
        capacity=1000
    )

    # Add distributor to supply chain
    supply_chain.add_distributor(
        name="USA Auto Distributors",
        location=ny_location
    )

    # Add retailer to supply chain
    supply_chain.add_retailer(
        name="Best Auto Sales",
        location=la_location
    )

    # Add car store to supply chain
    supply_chain.add_car_store(
        name="Luxury Auto Gallery",
        location=ny_location,
        brand="Tesla"
    )

    # Add warehouse to supply chain
    supply_chain.add_warehouse(
        location=texas_location,
        capacity=5000,
        manager="John Warehouse"
    )

    # Create order and process payment
    customer_order = Order(
        order_id="ORD123456",
        product=electric_car,
        quantity=1,
        price_per_unit=79999.99
    )
    customer_order.process_payment()
    customer_order.update_status("Shipped")

    # Create proxy for supplier management
    admin_proxy = SupplierManagerProxy("admin")
    user_proxy = SupplierManagerProxy("user")

    # Admin can add suppliers
    admin_proxy.add_supplier(battery_supplier)

    # Regular user can't add suppliers
    user_proxy.add_supplier(battery_supplier)  # Will print "Access denied"

    # Print information to demonstrate functionality
    print("\n=== Product Information ===")
    print(battery.get_info())
    print(engine.get_info())
    print(tire.get_info())

    print("\n=== Supplier Information ===")
    print(supplier_manager.get_supplier(local_supplier_id).get_info())
    print(supplier_manager.get_supplier(international_supplier_id).get_info())

    print("\n=== Manufacturer Information ===")
    print(auto_manufacturer.get_info())

    print("\n=== Warehouse Information ===")
    main_warehouse.check_inventory()

    print("\n=== Distributor Information ===")
    print(us_distributor.get_info())

    print("\n=== Retailer Information ===")
    print(auto_retailer.get_info())

    print("\n=== Car Store Information ===")
    print(premium_car_store.get_info())

    print("\n=== Maintenance Information ===")
    print(car_maintenance.get_info())

    print("\n=== Marketing Information ===")
    print(ev_marketing.get_info())

    print("\n=== Order Information ===")
    print(f"Order Status: {customer_order.status}")
    print(f"Order Value: ${customer_order.get_order_value():,.2f}")

    print("\n=== Supply Chain Status ===")
    print(supply_chain.get_supply_chain_status())

    # Run the user management system
    User.main()
