import sqlite3
from icecream import ic as print

# Global variable to track login status
current_user = None

class Retailer:
    def __init__(self, connection, user_id):
        self.conn = connection
        self.user_id = user_id
        
    def view_inventory(self):
        """View available inventory from distributors"""
        query = "SELECT * FROM inventory WHERE available_for_retailer = 1"
        items = self.conn.execute(query).fetchall()
        print("\nAvailable Inventory:")
        for item in items:
            print(f"ID: {item[0]}, Product: {item[1]}, Quantity: {item[2]}, Price: {item[3]}")
        return items
        
    def place_order(self, product_id, quantity):
        """Place an order with distributors"""
        try:
            with self.conn:
                # Check availability
                available = self.conn.execute(
                    "SELECT quantity FROM inventory WHERE id = ? AND available_for_retailer = 1",
                    (product_id,)
                ).fetchone()
                
                if available and available[0] >= quantity:
                    # Create order
                    self.conn.execute(
                        "INSERT INTO orders (product_id, retailer_id, quantity, status) VALUES (?, ?, ?, 'pending')",
                        (product_id, self.user_id, quantity)
                    )
                    # Update inventory
                    self.conn.execute(
                        "UPDATE inventory SET quantity = quantity - ? WHERE id = ?",
                        (quantity, product_id)
                    )
                    print(f"Order placed successfully for {quantity} units")
                else:
                    print("Insufficient inventory or product not available")
        except Exception as e:
            print(f"Error placing order: {e}")

class Distributor:
    def __init__(self, connection, user_id):
        self.conn = connection
        self.user_id = user_id
        
    def view_manufacturer_inventory(self):
        """View inventory from manufacturers"""
        query = "SELECT * FROM manufacturer_inventory WHERE available_for_distributor = 1"
        items = self.conn.execute(query).fetchall()
        print("\nManufacturer Inventory:")
        for item in items:
            print(f"ID: {item[0]}, Product: {item[1]}, Quantity: {item[2]}, Price: {item[3]}")
        return items
        
    def fulfill_retailer_orders(self):
        """View and fulfill retailer orders"""
        orders = self.conn.execute(
            "SELECT o.id, p.name, o.quantity, r.name FROM orders o "
            "JOIN products p ON o.product_id = p.id "
            "JOIN users r ON o.retailer_id = r.id "
            "WHERE o.status = 'pending'"
        ).fetchall()
        
        print("\nPending Orders:")
        for order in orders:
            print(f"Order ID: {order[0]}, Product: {order[1]}, Quantity: {order[2]}, Retailer: {order[3]}")
            
        order_id = input("Enter order ID to fulfill (or 0 to cancel): ")
        if order_id != '0':
            try:
                with self.conn:
                    self.conn.execute(
                        "UPDATE orders SET status = 'fulfilled', distributor_id = ? WHERE id = ?",
                        (self.user_id, order_id)
                    )
                    print("Order fulfilled successfully")
            except Exception as e:
                print(f"Error fulfilling order: {e}")
                
    def manage_inventory(self):
        """Add or update inventory for retailers"""
        print("\n1. Add new inventory\n2. Update existing inventory")
        choice = input("Select option: ")
        
        if choice == '1':
            product_name = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            
            try:
                with self.conn:
                    self.conn.execute(
                        "INSERT INTO inventory (product_name, quantity, price, available_for_retailer) VALUES (?, ?, ?, 1)",
                        (product_name, quantity, price)
                    )
                    print("Inventory added successfully")
            except Exception as e:
                print(f"Error adding inventory: {e}")
                
        elif choice == '2':
            items = self.conn.execute("SELECT id, product_name FROM inventory").fetchall()
            for item in items:
                print(f"ID: {item[0]}, Product: {item[1]}")
                
            item_id = input("Enter item ID to update: ")
            quantity = int(input("Enter new quantity: "))
            price = float(input("Enter new price: "))
            
            try:
                with self.conn:
                    self.conn.execute(
                        "UPDATE inventory SET quantity = ?, price = ? WHERE id = ?",
                        (quantity, price, item_id)
                    )
                    print("Inventory updated successfully")
            except Exception as e:
                print(f"Error updating inventory: {e}")

class Manufacturer:
    def __init__(self, connection, user_id):
        self.conn = connection
        self.user_id = user_id
        
    def produce_goods(self):
        """Add manufactured goods to inventory"""
        product_name = input("Enter product name: ")
        quantity = int(input("Enter quantity produced: "))
        cost = float(input("Enter production cost per unit: "))
        
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO manufacturer_inventory (product_name, quantity, cost, available_for_distributor) VALUES (?, ?, ?, 1)",
                    (product_name, quantity, cost)
                )
                print("Production recorded successfully")
        except Exception as e:
            print(f"Error recording production: {e}")
            
    def view_distributor_orders(self):
        """View orders from distributors"""
        orders = self.conn.execute(
            "SELECT o.id, p.name, o.quantity, d.name FROM manufacturer_orders o "
            "JOIN manufacturer_inventory p ON o.product_id = p.id "
            "JOIN users d ON o.distributor_id = d.id "
            "WHERE o.status = 'pending'"
        ).fetchall()
        
        print("\nPending Distributor Orders:")
        for order in orders:
            print(f"Order ID: {order[0]}, Product: {order[1]}, Quantity: {order[2]}, Distributor: {order[3]}")
            
        order_id = input("Enter order ID to fulfill (or 0 to cancel): ")
        if order_id != '0':
            try:
                with self.conn:
                    # Check inventory
                    product_id, quantity = self.conn.execute(
                        "SELECT product_id, quantity FROM manufacturer_orders WHERE id = ?",
                        (order_id,)
                    ).fetchone()
                    
                    available = self.conn.execute(
                        "SELECT quantity FROM manufacturer_inventory WHERE id = ?",
                        (product_id,)
                    ).fetchone()
                    
                    if available and available[0] >= quantity:
                        self.conn.execute(
                            "UPDATE manufacturer_orders SET status = 'fulfilled', manufacturer_id = ? WHERE id = ?",
                            (self.user_id, order_id)
                        )
                        self.conn.execute(
                            "UPDATE manufacturer_inventory SET quantity = quantity - ? WHERE id = ?",
                            (quantity, product_id)
                        )
                        print("Order fulfilled successfully")
                    else:
                        print("Insufficient inventory to fulfill order")
            except Exception as e:
                print(f"Error fulfilling order: {e}")
                


def login(connection):
    global current_user
    print("\n--- Supply Chain Login ---")
    username = input("Username: ")
    password = input("Password: ")  # In production, use hashed passwords
    
    user = connection.execute(
        "SELECT id, username, name, role FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    
    if user:
        current_user = {
            'id': user[0],
            'username': user[1],
            'name': user[2],
            'role': user[3]
        }
        print(f"\nWelcome {current_user['name']} ({current_user['role'].title()})!")
        return True
    else:
        print("Invalid username or password!")
        return False

def logout():
    global current_user
    if current_user:
        print(f"Goodbye {current_user['name']}!")
        current_user = None
    else:
        print("No user is currently logged in.")

def show_retailer_dashboard(connection):
    retailer = Retailer(connection, current_user['id'])
    while True:
        print("\n=== RETAILER DASHBOARD ===")
        print("1. View Available Inventory")
        print("2. Place Order")
        print("3. View My Orders")
        print("4. Logout")
        
        choice = input("Select option: ")
        
        if choice == '1':
            retailer.view_inventory()
        elif choice == '2':
            product_id = input("Enter product ID: ")
            quantity = input("Enter quantity: ")
            retailer.place_order(int(product_id), int(quantity))
        elif choice == '3':
            orders = connection.execute(
                "SELECT o.id, p.product_name, o.quantity, o.status FROM orders o "
                "JOIN inventory p ON o.product_id = p.id "
                "WHERE o.retailer_id = ?",
                (current_user['id'],)
            ).fetchall()
            
            print("\nYour Orders:")
            for order in orders:
                print(f"ID: {order[0]}, Product: {order[1]}, Qty: {order[2]}, Status: {order[3]}")
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid option!")

def show_distributor_dashboard(connection):
    distributor = Distributor(connection, current_user['id'])
    while True:
        print("\n=== DISTRIBUTOR DASHBOARD ===")
        print("1. View Manufacturer Inventory")
        print("2. Fulfill Retailer Orders")
        print("3. Manage Inventory")
        print("4. View All Orders")
        print("5. Logout")
        
        choice = input("Select option: ")
        
        if choice == '1':
            distributor.view_manufacturer_inventory()
        elif choice == '2':
            distributor.fulfill_retailer_orders()
        elif choice == '3':
            distributor.manage_inventory()
        elif choice == '4':
            orders = connection.execute(
                "SELECT o.id, r.name, p.product_name, o.quantity, o.status FROM orders o "
                "JOIN users r ON o.retailer_id = r.id "
                "JOIN inventory p ON o.product_id = p.id"
            ).fetchall()
            
            print("\nAll Orders:")
            for order in orders:
                print(f"ID: {order[0]}, Retailer: {order[1]}, Product: {order[2]}, Qty: {order[3]}, Status: {order[4]}")
        elif choice == '5':
            logout()
            break
        else:
            print("Invalid option!")

def show_manufacturer_dashboard(connection):
    manufacturer = Manufacturer(connection, current_user['id'])
    while True:
        print("\n=== MANUFACTURER DASHBOARD ===")
        print("1. Produce Goods")
        print("2. View Distributor Orders")
        print("3. View Production Inventory")
        print("4. Logout")
        
        choice = input("Select option: ")
        
        if choice == '1':
            manufacturer.produce_goods()
        elif choice == '2':
            manufacturer.view_distributor_orders()
        elif choice == '3':
            inventory = connection.execute(
                "SELECT id, product_name, quantity, cost FROM manufacturer_inventory"
            ).fetchall()
            
            print("\nProduction Inventory:")
            for item in inventory:
                print(f"ID: {item[0]}, Product: {item[1]}, Qty: {item[2]}, Cost: {item[3]}")
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid option!")

def initialize_database(connection):
    """Create tables and add sample data if they don't exist"""
    queries = [
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('retailer', 'distributor', 'manufacturer')),
            email TEXT UNIQUE
        )""",
        """CREATE TABLE IF NOT EXISTS manufacturer_inventory (
            id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            cost REAL NOT NULL,
            available_for_distributor INTEGER DEFAULT 0
        )""",
        """CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            available_for_retailer INTEGER DEFAULT 0
        )""",
        """CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            retailer_id INTEGER NOT NULL,
            distributor_id INTEGER,
            quantity INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(product_id) REFERENCES inventory(id),
            FOREIGN KEY(retailer_id) REFERENCES users(id),
            FOREIGN KEY(distributor_id) REFERENCES users(id)
        )""",
        """CREATE TABLE IF NOT EXISTS manufacturer_orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            distributor_id INTEGER NOT NULL,
            manufacturer_id INTEGER,
            quantity INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(product_id) REFERENCES manufacturer_inventory(id),
            FOREIGN KEY(distributor_id) REFERENCES users(id),
            FOREIGN KEY(manufacturer_id) REFERENCES users(id)
        )"""
    ]
    
    try:
        with connection:
            for query in queries:
                connection.execute(query)
            
            # Add sample users if they don't exist
            connection.execute(
                "INSERT OR IGNORE INTO users VALUES (1, 'retailer1', 'pass123', 'ABC Store', 'retailer', 'retailer@example.com')"
            )
            connection.execute(
                "INSERT OR IGNORE INTO users VALUES (2, 'distributor1', 'pass123', 'XYZ Distributors', 'distributor', 'distributor@example.com')"
            )
            connection.execute(
                "INSERT OR IGNORE INTO users VALUES (3, 'manufacturer1', 'pass123', 'Global Manufacturers', 'manufacturer', 'manufacturer@example.com')"
            )
            
            # Add sample inventory
            connection.execute(
                "INSERT OR IGNORE INTO manufacturer_inventory VALUES (1, 'Widget A', 100, 5.99, 1)"
            )
            connection.execute(
                "INSERT OR IGNORE INTO inventory VALUES (1, 'Widget A Retail', 50, 9.99, 1)"
            )
            
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
def get_connection(db_name):
    try: 
        return sqlite3.connect(db_name)
    except Exception as e: 
        print(f"exception1 {e}")
        raise

def main():
    
    
    conn = get_connection("supply_chain.db")
    initialize_database(conn)
    
    while True:
        if current_user:
            if current_user['role'] == 'retailer':
                show_retailer_dashboard(conn)
            elif current_user['role'] == 'distributor':
                show_distributor_dashboard(conn)
            elif current_user['role'] == 'manufacturer':
                show_manufacturer_dashboard(conn)
        else:
            print("\n=== Supply Chain Management System ===")
            print("1. Login")
            print("2. Exit")
            
            choice = input("Select option: ")
            
            if choice == '1':
                if login(conn):
                    continue
            elif choice == '2':
                print("Exiting system...")
                break
            else:
                print("Invalid option!")
    
    conn.close()

if __name__ == "__main__":
    main()
    
def get_connection(db_name):
    try: 
        return sqlite3.connect(db_name)
    except Exception as e: 
        print(f"exception1 {e}")
        raise
