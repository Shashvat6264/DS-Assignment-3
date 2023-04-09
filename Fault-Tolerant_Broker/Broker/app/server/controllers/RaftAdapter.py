from ..raft import RaftNode
import pickle
import time

class RaftAdapter:
    def __init__(self, raft_server: RaftNode, partition):
        self.__raft_server = raft_server
        self.__partition = partition
    
    def get_state(self):
        state = self.__raft_server.check_committed_entry()
        if state is not None:
            if str(self.__partition.getId()) not in state:
                return {
                    'queue': [],
                    'consumerOffsets': {}
                }
            partition_state = state[str(self.__partition.getId())]
            if isinstance(partition_state, dict):
                return partition_state
            return None
        else:
            return None
        
    def update_state(self, state):
        complete_state = self.__raft_server.check_committed_entry()
        complete_state[str(self.__partition.getId())] = state
        self.__raft_server.client_request(complete_state)
        time.sleep(5)
        
    def set_raft_server(self, raft_server):
        self.__raft_server = raft_server
        
        
    
        