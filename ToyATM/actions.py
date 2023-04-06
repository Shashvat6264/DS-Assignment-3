from exceptions import *
class Action:
    def run(self, *args, **kwargs):
        pass
    
    def flow(self):
        pass
    
    def output(self, *args, **kwargs):
        pass

class WithdrawAction(Action):
    def run(self, *args, **kwargs):
        balances = kwargs["balances"]
        name = kwargs["name"]
        amount = kwargs["amount"]
        new_balances = balances.copy()
        if name not in new_balances:
            raise NameNotFound(f"{name} not found in the ATM")
        if amount > new_balances[name]:
            raise NotEnoughMoney(f"{name} does not have {amount} to withdraw")
        new_balances[name] -= amount
        return {"amount": new_balances[name]}, new_balances
    
    def flow(self):
        args = {}
        print("""<--- Withdraw --->""")
        amount = int(input("Enter amount to withdraw: "))
        args["amount"] = amount
        return args
    
    def output(self, *args, **kwargs):
        amount = kwargs["amount"]
        name = kwargs["name"]
        print(f"""Withdraw successful
---> Balance amount in {name}: {amount}""")
    
class DepositAction(Action):
    def run(self, *args, **kwargs):
        balances = kwargs["balances"]
        name = kwargs["name"]
        amount = kwargs["amount"]
        new_balances = balances.copy()
        if name not in new_balances:
            new_balances[name] = 0
        new_balances[name] += amount
        return {"amount": new_balances[name]}, new_balances
    
    def flow(self):
        args = {}
        print("""<--- Deposit --->""")
        amount = int(input("Enter amount to deposit: "))
        args["amount"] = amount
        return args
    
    def output(self, *args, **kwargs):
        amount = kwargs["amount"]
        name = kwargs["name"]
        print(f"""Deposit successful
---> Balance amount in {name}: {amount}""")
    
class EnquireAction(Action):
    def run(self, *args, **kwargs):
        balances = kwargs["balances"]
        name = kwargs["name"]
        if name not in balances:
            balances[name] = 0
        return {"amount": balances[name]}, balances
    
    def flow(self):
        print("""<--- Balance Enquiry --->""")
        return {}
    
    def output(self, *args, **kwargs):
        amount = kwargs["amount"]
        name = kwargs["name"]
        print(f"""Enquiry successful
---> Balance amount in {name}: {amount}""")

class TransferAction(Action):
    def run(self, *args, **kwargs):
        balances = kwargs["balances"]
        name = kwargs["name"]
        receiver = kwargs["receiver"]
        amount = kwargs["amount"]
        new_balances = balances.copy()
        if name not in new_balances:
            raise NameNotFound(f"{name} not found in ATM")
        if amount > new_balances[name]:
            raise NotEnoughMoney(f"{name} does not have {amount} to transfer")
        new_balances[name] -= amount
        if receiver not in new_balances:
            new_balances[receiver] = 0
        new_balances[receiver] += amount
        return {"name_amount": new_balances[name], "receiver_amount": new_balances[receiver], "receiver": receiver}, new_balances
    
    def flow(self):
        args = {}
        print("""<--- Fund Transfer --->""")
        
        amount = int(input("Enter amount to transfer: "))
        receiver = str(input("Provide reciver name: "))
        
        args["amount"] = amount
        args["receiver"] = receiver
        return args
    
    def output(self, *args, **kwargs):
        name_amount = kwargs["name_amount"]
        receiver_amount = kwargs["receiver_amount"]
        name = kwargs["name"]
        receiver = kwargs["receiver"]
        print(f"""Transfer successful
---> Balance amount in {name}: {name_amount}
---> Balance amount in {receiver}: {receiver_amount}""")