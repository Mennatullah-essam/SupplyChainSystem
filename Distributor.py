class Distributor:
    def __init__(self, distributor_id, name, distribution_network):
        self.distributor_id = distributor_id
        self.name = name
        self.distribution_network = distribution_network  # List of locations the distributor covers
        self.inventory = {}  # Initializes inventory as an empty dictionary

    def get_total_quantity(self):
        # Calculate the total quantity of products in the distributor's inventory
        return sum(self.inventory.values())

    def distribute_product(self, product_id, product_quantity, retailer):
        # Send products to a retailer
        if product_id in self.inventory and product_quantity <= self.inventory[product_id]:
            self.inventory[product_id] -= product_quantity
            retailer.receive_product(product_id, product_quantity)
            print(f"{product_quantity} units of product {product_id} distributed to {retailer.name}.")
            
            if self.inventory[product_id] == 0:
                del self.inventory[product_id]
                print(f"Product {product_id} is now out of stock at the distributor.")
        else:
            print("Not enough stock available or product not found!")

    def receive_product(self, product_id, product_quantity):
        # Receive products into the distributor's inventory
        if product_quantity <= 0:
            print("Quantity must be positive!")
            return

        if product_id in self.inventory:
            self.inventory[product_id] += product_quantity
        else:
            self.inventory[product_id] = product_quantity
        
        print(f"{product_quantity} units of product {product_id} received into distributor inventory.")

    def receive_from_warehouse(self, warehouse, product_id, product_quantity):
        # Transfer products from warehouse to distributor
        if product_id in warehouse.inventory and product_quantity <= warehouse.inventory[product_id]:
            warehouse.retrieve_product(product_id, product_quantity)
            self.receive_product(product_id, product_quantity)
            print(f"{product_quantity} units of product {product_id} received from warehouse {warehouse.warehouse_id}.")
        else:
            print("Not enough stock in the warehouse or product not found!")

    def get_distributor_info(self):
        # Display distributor information
        print(f"Distributor ID: {self.distributor_id}")
        print(f"Name: {self.name}")
        print(f"Distribution Network: {', '.join(self.distribution_network)}")
        self.check_inventory()

    def check_inventory(self):
        # Display the current inventory
        if not self.inventory:
            print("The distributor's inventory is empty.")
        else:
            print("Current Inventory:")
            for product_id, product_quantity in self.inventory.items():
                print(f"- Product ID {product_id}: {product_quantity} units")

# Let me know if you want any adjustments or more features added! 🚀
