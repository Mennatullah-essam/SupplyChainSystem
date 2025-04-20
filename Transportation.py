class Transportation:
    def __init__(self, transport_id, source, destination, vehicle_type):
        self.transport_id = transport_id
        self.source = source
        self.destination = destination
        self.vehicle_type = vehicle_type
        self.cars = {}  
        self.status = "Pending"

    def add_car(self, model, brand, quantity, car_type):
        """Add a car to the transport dictionary"""
        car_id = f"{brand} {model}"  # Combine brand and model as unique car ID
        if car_id in self.cars:
            self.cars[car_id]['quantity'] += quantity  # Add to existing quantity if car is already in the list
        else:
            self.cars[car_id] = {
                'quantity': quantity,
                'type': car_type
            }
        print(f"Added {quantity} {brand} {model} cars of type '{car_type}' to the transport list.")

    def list_cars(self):
        """Display the list of cars being transported"""
        if not self.cars:
            print("No cars in the transport list.")
        else:
            print(f"Cars being transported from {self.source} to {self.destination}:")
            for car_id, details in self.cars.items():
                print(f"- {details['quantity']} cars of {car_id} ({details['type']})")

    def start_transport(self):
        if not self.cars:
            print("No cars to transport.")
        else:
            self.status = "In Transit"
            print(f"Transport {self.transport_id} started from {self.source} to {self.destination} using {self.vehicle_type}.")

    def complete_transport(self):
        if self.status != "In Transit":
            print("Transport hasn't started or is already completed.")
        else:
            self.status = "Delivered"
            print(f"Transport {self.transport_id} has been delivered to {self.destination}.")

    def get_status(self):
        return self.status

    def get_details(self):
        print(f"Transport ID: {self.transport_id}")
        print(f"From: {self.source}")
        print(f"To: {self.destination}")
        print(f"Cars: {self.cars}")
        print(f"Vehicle Type: {self.vehicle_type}")
        print(f"Status: {self.status}")
