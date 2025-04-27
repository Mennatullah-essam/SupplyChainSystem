class Product:
    def init(self, product_id, name, category, price, quantity, manufacture_date, warranty_years):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.manufacture_date = manufacture_date
        self.warranty_years = warranty_years

    def update_quantity(self, amount):
        self.quantity += amount

    def get_info(self):
        return {
            "Product ID": self.product_id,
            "Name": self.name,
            "Category": self.category,
            "Price": self.price,
            "Quantity": self.quantity,
            "Manufacture Date": self.manufacture_date,
            "Warranty (Years)": self.warranty_years
        }

class Manufacturer:
    def init(self, manufacturer_id, name, production_capacity):
        self.manufacturer_id = manufacturer_id
        self.name = name
        self.raw_materials = []
        self.products_produced = []
        self.production_capacity = production_capacity
        self.product_counter = 0

    def add_raw_material(self, product):
        self.raw_materials.append(product)

    def manufacture_product(self, product_name, category, price, quantity=1, manufacture_date=None, warranty_years=0):
        if self.product_counter < self.production_capacity:
            self.product_counter += 1
            product_id = f"{product_name[:3].upper()}{self.product_counter}"
            new_product = Product(product_id, product_name, category, price, quantity, manufacture_date, warranty_years)
            self.products_produced.append(new_product)
            return new_product
        else:
            print("Production capacity reached!")
            return None

    def get_manufacturer_info(self):
        return {
            "Manufacturer ID": self.manufacturer_id,
            "Name": self.name,
            "Production Capacity": self.production_capacity,
            "Products Produced": [p.get_info() for p in self.products_produced]
        }

class Maintenance:
    def init(self, maintenance_id, product, date, service_type, service_details, cost, parts_replaced=None):
        self.maintenance_id = maintenance_id
        self.product = product
        self.date = date
        self.service_type = service_type
        self.service_details = service_details
        self.cost = cost
        self.parts_replaced = parts_replaced if parts_replaced else []

    def get_maintenance_record(self):
        return {
            "Maintenance ID": self.maintenance_id,
            "Car ID": self.product.product_id,
            "Car Name": self.product.name,
            "Date": self.date,
            "Service Type": self.service_type,
            "Details": self.service_details,
            "Cost": self.cost,
            "Parts Replaced": self.parts_replaced
        }

    def str(self):
        return f"[{self.date}] {self.product.name} - {self.service_type}: ${self.cost}"
