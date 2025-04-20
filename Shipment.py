class Shipment:
    def __init__(self, shipment_id, supplier, destination_warehouse, products, shipment_date, expected_arrival, status):
        self.shipment_id = shipment_id
        self.supplier = supplier
        self.destination_warehouse = destination_warehouse
        self.products = products
        self.shipment_date = shipment_date
        self.expected_arrival = expected_arrival
        self.status = status

    def get_shipment_details(self):
        product_details = ""
        for p_id, qty in self.products.items():
            product_details += f"- {p_id}: {qty} units\n"
        return (
            f"Shipment ID: {self.shipment_id}\n"
            f"Supplier: {self.supplier.name}\n"
            f"Destination Warehouse: {self.destination_warehouse.location}\n"
            f"Shipment Date: {self.shipment_date}\n"
            f"Expected Arrival: {self.expected_arrival}\n"
            f"Status: {self.status}\n"
            f"Products:\n{product_details}"
        )

    def deliver(self):
        if self.status != "Delivered":
            if self.destination_warehouse:
                for product_id, quantity in self.products.items():
                    self.destination_warehouse.store_product(product_id, quantity)
                self.status = "Delivered"
                print(f"Shipment {self.shipment_id} delivered.")
            else:
                print("Destination warehouse not found.")
        else:
            print(f"Shipment {self.shipment_id} already delivered.")

    def update_status(self, new_status):
        self.status = new_status
        print(f"Shipment {self.shipment_id} status updated to {new_status}.")
