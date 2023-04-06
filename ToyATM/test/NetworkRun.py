
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import ATM

ip_addr = "127.0.0.1"
comm_dict = {"node0": {"ip": ip_addr, "port": "5567"}, 
             "node1": {"ip": ip_addr, "port": "5566"}, 
             "node2": {"ip": ip_addr, "port": "5565"}}

atm = ATM.ATMInterface(comm_dict, str(sys.argv[1]))
atm.start()
