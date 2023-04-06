from raft import RaftNode
import time
from actions import *

class ATMBloc:
    def __init__(self, name, raftnode):
        self.__name = name
        self.__raftnode = raftnode
        self.__actions = [WithdrawAction(), DepositAction(), EnquireAction(), TransferAction()]
    
    def init_balances(self):
        self.__update_balances({})
    
    def __get_balances(self):
        balances = self.__raftnode.check_committed_entry()
        if balances == "Init Entry":
            self.__update_balances({})
            return {}
        return balances
    
    def __update_balances(self, balances):
        self.__raftnode.client_request(balances)
        time.sleep(7)
    
    def run_action(self, action_id, args):
        args["balances"] = self.__get_balances()
        return_value, new_balances = self.__actions[action_id].run(**args)
        self.__update_balances(new_balances)
        return return_value
    
    def flow_action(self, action_id):
        return self.__actions[action_id].flow()
    
    def output_action(self, action_id, return_value):
        self.__actions[action_id].output(**return_value)
    

class ATMInterface:
    def __init__(self, comm_dict, name):
        self._raftNode = RaftNode(comm_dict, name, verbose=False)
        self._bloc = ATMBloc(name, self._raftNode)
        
    def start(self):
        self._raftNode.start()
        
        time.sleep(5)
        self._bloc.init_balances()
        
        while True:
            print("<--- Welcome to Toy ATM --->")
            name = str(input("Enter your name: "))
            
            print("""
Action Menu:
----> 0: Withdraw money
----> 1: Deposit money
----> 2: Balance inquiry
----> 3: Transfer
                  """)
            
            action_id = int(input("Enter number of action to be performed: "))
            args = self._bloc.flow_action(action_id)
            args["name"] = name
            try:
                print("-----> Transaction in Progress")
                return_value = self._bloc.run_action(action_id, args)
            except Exception as e:
                print(str(e))
                continue
            return_value["name"] = name
            self._bloc.output_action(action_id, return_value)
            
            
            
            