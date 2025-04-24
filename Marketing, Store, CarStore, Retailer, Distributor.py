# Marketing Class: Handles marketing strategies and campaigns
class Marketing:
    def __init__(self, strategy, budget):
        self.__strategy = strategy  
        self.__budget = budget  
        self.__reach = 0  

    def run_campaign(self):
        multipliers = {
            "Social Media": 75,
            "TV Ads": 120,
            "Billboards": 50,
            "Email Marketing": 40
        }
        try:
            if self.__strategy in multipliers:
                self.__reach = self.__budget * multipliers[self.__strategy]
            else:
                self.__reach = self.__budget * 60
            print(f"Running a {self.__strategy} campaign with a budget of ${self.__budget}. Estimated reach: {self.__reach} people.")
        except TypeError as e:
            print(f"[Type Error in campaign]: {e}")
        except Exception as e:
            print(f"[Unknown error in campaign]: {e}")

    def analyze_market(self):
        try:
            if self.__reach > 100000:
                trend = "High Demand"
            elif self.__reach > 50000:
                trend = "Stable Market"
            else:
                trend = "Low Interest"
            print(f"Market Analysis: Based on campaign reach, current trend is {trend}.")
            return trend
        except AttributeError as e:
            print(f"[Attribute Error in analysis]: {e}")
            return None
        except Exception as e:
            print(f"[Unknown error in analysis]: {e}")
            return None


# Base Class for Stores
class Store:
    def __init__(self, store_id, name, location):
        self.__store_id = store_id
        self.__name = name
        self.__location = location
        self.__stock = []

    def add_car(self, car):
        try:
            self.__stock.append(car)
            print(f"Added {car} to {self.__name} store.")
        except AttributeError as e:
            print(f"[Attribute Error adding car]: {e}")
        except Exception as e:
            print(f"[Unknown error adding car]: {e}")

    def sell_car(self, car):
        try:
            if car in self.__stock:
                self.__stock.remove(car)
                print(f"Sold {car} from {self.__name} store.")
            else:
                raise ValueError(f"{car} is not available in {self.__name} store.")
        except ValueError as e:
            print(f"[Value Error selling car]: {e}")
        except Exception as e:
            print(f"[Unknown error selling car]: {e}")

    def check_stock(self):
        return len(self.__stock)

    def get_name(self):
        return self.__name

    def get_stock(self):
        return self.__stock


# CarStore Class: Represents a car dealership
class CarStore(Store):
    def purchase_from_retailer(self, retailer, car):
        try:
            if car in retailer.get_stock():
                retailer.sell_car(car)
                self.add_car(car)
                print(f"{self.get_name()} purchased {car} from {retailer.get_name()}.")
            else:
                raise ValueError(f"{car} is not available at {retailer.get_name()}.")
        except ValueError as e:
            print(f"[Value Error purchasing car]: {e}")
        except Exception as e:
            print(f"[Unknown error purchasing car]: {e}")


# Retailer Class
class Retailer(Store):
    def __init__(self, retailer_id, name, location):
        super().__init__(retailer_id, name, location)

    def order_product(self, distributor, car, quantity):
        try:
            print(f"Retailer {self.get_name()} ordering {quantity} of {car} from Distributor {distributor.get_name()}.")
            order_id = distributor.generate_order_id()
            order = Order(order_id, car, quantity, 100000)  # Added default price_per_unit
            order.place_order()
            distributor.distribute_product(self, car, quantity, order)
            return order
        except AttributeError as e:
            print(f"[Attribute Error ordering product]: {e}")
        except Exception as e:
            print(f"[Unknown error ordering product]: {e}")

    def receive_product(self, car):
        self.add_car(car)

    def sell_product(self, car):
        self.sell_car(car)

    def check_stock(self):
        try:
            stock = self.get_stock()
            print(f"Available cars in {self.get_name()}: {len(stock)}")
            return stock
        except AttributeError as e:
            print(f"[Attribute Error checking stock]: {e}")
            return []
        except Exception as e:
            print(f"[Unknown error checking stock]: {e}")
            return []

    def return_car(self, distributor, car):
        try:
            if car in self.get_stock():
                self.sell_car(car)
                distributor.add_to_inventory(car)
                print(f"{car} returned to Distributor {distributor.get_name()}.")
            else:
                raise ValueError(f"{car} is not available for return in {self.get_name()} store.")
        except ValueError as e:
            print(f"[Value Error returning car]: {e}")
        except Exception as e:
            print(f"[Unknown error returning car]: {e}")


# Distributor Class
class Distributor:
    def __init__(self, distributor_id, name, distribution_network=None):
        self.__distributor_id = distributor_id
        self.__name = name
        self.__distribution_network = distribution_network
        self.__inventory = []
        self.__order_count = 0

    def add_to_inventory(self, car):
        try:
            self.__inventory.append(car)
            print(f"Added {car} to Distributor {self.__name}'s inventory.")
        except AttributeError as e:
            print(f"[Attribute Error adding to inventory]: {e}")
        except Exception as e:
            print(f"[Unknown error adding to inventory]: {e}")

    def distribute_product(self, retailer, car, quantity, order):
        try:
            available_quantity = self.__inventory.count(car)
            if available_quantity >= quantity:
                for _ in range(quantity):
                    self.__inventory.remove(car)
                    retailer.receive_product(car)
                order.update_order_status("Shipped")
                print(f"Distributed {quantity} of {car} to Retailer {retailer.get_name()}.")
            else:
                print(f"Not enough {car} in Distributor {self.__name}'s inventory.")
                order.update_order_status("Cancelled")
        except ValueError as e:
            print(f"[Value Error distributing product]: {e}")
        except Exception as e:
            print(f"[Unknown error distributing product]: {e}")

    def get_distributor_info(self):
        return {
            "ID": self.__distributor_id,
            "Name": self.__name,
            "Network": self.__distribution_network,
            "Inventory": self.__inventory
        }

    def get_name(self):
        return self.__name

    def generate_order_id(self):
        self.__order_count += 1
        return self.__order_count


# Order Class
class Order:
    def __init__(self, order_id, product, quantity, price_per_unit):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.status = "Pending"
        self.date = "Today"
        self.estimated_delivery_days = self.calculate_delivery_time()

    def place_order(self):
        print(f"Order {self.order_id} placed for {self.quantity} of {self.product} at {self.price_per_unit} EGP each.")

    def update_order_status(self, new_status):
        self.status = new_status
        print(f"Order {self.order_id} status updated to {self.status}.")

    def track_order(self):
        print(f"Order {self.order_id} - {self.product} | Quantity: {self.quantity} | Status: {self.status} | Expected Delivery: {self.estimated_delivery_days} days.")

    def calculate_total_price(self):
        return self.quantity * self.price_per_unit

    def calculate_delivery_time(self):
        if self.product == "Tesla Model S":
            return 3
        elif self.product == "BMW i8":
            return 4
        else:
            return 5


# Test system
marketing = Marketing("Social Media", 5000)
marketing.run_campaign()
market_trend = marketing.analyze_market()

distributor = Distributor(101, "Auto Distributors", ["North Egypt", "Delta"])
retailer = Retailer(201, "City Cars", "Cairo")
car_store = CarStore(301, "Elite Motors", "Alexandria")

distributor.add_to_inventory("Tesla Model S")
distributor.add_to_inventory("Tesla Model S")
distributor.add_to_inventory("BMW i8")

order1 = retailer.order_product(distributor, "Tesla Model S", 2)
order1.track_order()
print(f"Total price: {order1.calculate_total_price()} EGP")

order2 = retailer.order_product(distributor, "BMW i8", 1)
order2.track_order()
print(f"Total price: {order2.calculate_total_price()} EGP")

order3 = retailer.order_product(distributor, "Audi A6", 1)
order3.track_order()
print(f"Total price: {order3.calculate_total_price()} EGP")

retailer.check_stock()

retailer.sell_product("Tesla Model S")
retailer.check_stock()

retailer.return_car(distributor, "BMW i8")

car_store.purchase_from_retailer(retailer, "Tesla Model S")
print(f"{car_store.get_name()} stock: {car_store.check_stock()} cars available.")
