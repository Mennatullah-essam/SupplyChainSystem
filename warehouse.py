class Warehouse:
    def __init__(self, warehouse_id, location, capacity):
        self.warehouse_id = warehouse_id
        self.location = location
        self.capacity = capacity
        self.inventory = {}  # Stores products as {product_id: product_quantity}

    def get_total_quantity(self):
        # Calculate the total quantity of products in the warehouse
        return sum(self.inventory.values())

    def store_product(self, product_id, product_quantity):
        # Add products to the warehouse inventory, considering capacity.
        if product_quantity <= 0:
            print("Quantity must be positive!")
            return

        if product_id in self.inventory:
            # Update quantity if product already exists
            if self.get_total_quantity() + product_quantity <= self.capacity:
                self.inventory[product_id] += product_quantity
                print(f"{product_quantity} units of product {product_id} added to inventory.")
            else:
                print("Not enough space in the warehouse!")
        else:
            # Add new product if not already in inventory
            if self.get_total_quantity() + product_quantity <= self.capacity:
                self.inventory[product_id] = product_quantity
                print(f"{product_quantity} units of product {product_id} added to inventory.")
            else:
                print("Not enough space in the warehouse!")

    def retrieve_product(self, product_id, product_quantity):
        # Retrieve products from inventory.
        if product_id in self.inventory:
            if product_quantity <= self.inventory[product_id]:
                self.inventory[product_id] -= product_quantity
                print(f"{product_quantity} units of product {product_id} retrieved from inventory.")
                # Remove product if quantity becomes zero
                if self.inventory[product_id] == 0:
                    del self.inventory[product_id]
                    print(f"Product {product_id} is now out of stock in the warehouse.")
            else:
                print("Not enough stock available!")
        else:
            print("Product not found in inventory!")

    def check_inventory(self):
        # Display the current inventory.
        if not self.inventory:
            print("The warehouse is empty.")
        else:
            print(f"Inventory in Warehouse {self.warehouse_id}:")
            for product_id, product_quantity in self.inventory.items():
                print(f"- Product ID {product_id}: {product_quantity} units")