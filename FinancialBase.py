class FinancialBase:
    def __init__(self, manager_id, name, department):
        # Initialize financial base attributes
        self.manager_id = manager_id
        self.name = name
        self.department = department
        self.budget = 0.0
        self.expenses = 0.0
        self.revenue = 0.0
    
    def allocate_budget(self, amount):
        # Add amount to budget
        self.budget += amount
    
    def record_expense(self, amount, description):
        # Record an expense and deduct from budget
        if amount <= self.budget:
            self.expenses += amount
            self.budget -= amount
    
    def record_revenue(self, amount, source):
        # Record revenue and add to budget
        self.revenue += amount
        self.budget += amount


class FinancialManager(FinancialBase):
    def __init__(self, manager_id, name, department):
        # Initialize financial manager with additional attributes
        super().__init__(manager_id, name, department)
        self.salaries = {}
        self.tax_rate = 0.15
        self.insurance_costs = 0.0
    
    def add_salary(self, employee_id, amount):
        # Add salary for an employee
        self.salaries[employee_id] = amount
    
    def calculate_taxes(self):
        # Calculate taxes based on revenue
        return self.revenue * self.tax_rate
    
    def add_insurance_cost(self, amount):
        # Add insurance cost and include in expenses
        self.insurance_costs += amount
        self.expenses += amount
    
    def record_expense(self, amount, description):
        # Override: Validate and record expense
        try:
            if amount < 0:
                raise ValueError("Invalid expense amount!")
            super().record_expense(amount, description)
        except ValueError as e:
            print(f"Error recording expense: {e}")
    
    def record_revenue(self, amount, source):
        # Override: Validate and record revenue
        try:
            if amount < 0:
                raise ValueError("Invalid revenue amount!")
            super().record_revenue(amount, source)
        except ValueError as e:
            print(f"Error recording revenue: {e}")


class Invoice:
    def __init__(self, invoice_id, customer, vehicle, amount):
        # Initialize invoice details
        self.invoice_id = invoice_id
        self.customer = customer
        self.vehicle = vehicle
        self.amount = amount
        self.status = "Pending"
    
    def mark_as_paid(self):
        # Mark invoice as paid
        self.status = "Paid"
    
    def __str__(self):
        # Return formatted invoice details
        return f"Invoice[{self.invoice_id}] - {self.customer} for {self.vehicle.model}, Amount: ${self.amount}, Status: {self.status}"


class FinancialReport:
    def __init__(self, financial_manager):
        # Initialize financial report with a financial manager instance
        self.financial_manager = financial_manager
    
    def generate_report(self):
        # Generate and return financial report details
        net_profit = self.financial_manager.revenue - self.financial_manager.expenses
        taxes = self.financial_manager.calculate_taxes()
        return (f"Financial Report\n"
                f"Manager: {self.financial_manager.name}, Department: {self.financial_manager.department}\n"
                f"Budget: ${self.financial_manager.budget}, Expenses: ${self.financial_manager.expenses}, Revenue: ${self.financial_manager.revenue}\n"
                f"Net Profit: ${net_profit}, Taxes: ${taxes}, Insurance Costs: ${self.financial_manager.insurance_costs}")
