from ..raft import RaftNode, Listener, Talker
import os
import time

class CustomRaftNode(RaftNode):
    def __init__(self, config, name, role='follower', verbose=True):
        super().__init__(config, name, role, verbose)
        self.__config = config
    
    async def addNode(self, node, address):
        if address in self.__config:
            return self
        
        super().stop()

        self.__config[address] = node
        
        CURRENT_ADDRESS = os.getenv('CURRENT_ADDRESS')
        
        new_raft_node = CustomRaftNode(self.__config, CURRENT_ADDRESS, verbose=False)
        new_raft_node.start()
        time.sleep(5)
        return new_raft_node
        