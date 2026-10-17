class BankAccount: 
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance # _ means private — don't touch directly 
    
    def get_balance(self):
        return self._balance
        
    def deposit(self, amount):
            if amount > 0: 
                self._balance += amount 
            else: 
                print("Deposit must be positive.")
