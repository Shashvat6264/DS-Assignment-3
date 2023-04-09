from .Queue import Queue
from .Message import Message
from .RaftAdapter import RaftAdapter
from .exceptions import *

class RaftQueue(Queue):
    def __init__(self, raft: RaftAdapter):
        super().__init__()
        self.__raft = raft
        
    def __get_queue(self):
        state = self.__raft.get_state()
        if state is not None:
            return state['queue'], state
        else:
            return None, None
        
    def __update_queue(self, queue, state = None):
        if state is None:
            state = self.__raft.get_state()
            if state is None:
                return
        state['queue'] = queue
        self.__raft.update_state(state)
        
    async def push(self, message: Message) -> int:
        queue, state = self.__get_queue()
        if queue is not None:
            queue.append(message.toJSON())
            id = len(queue) - 1
            self.__update_queue(queue, state)
            return id
        else:
            return -1
        
    async def getIndex(self, index: int) -> Message:
        queue, _ = self.__get_queue()
        if queue is not None:
            if index <= len(queue) - 1:
                return Message.fromJSON(queue[index])
            else:
                raise QueueEmpty(message="Index not available in queue")
        return None
    
    async def pop(self) -> Message:
        queue, state = self.__get_queue()
        if queue.isEmpty():
            raise QueueEmpty(message="Queue is empty")
        message = queue[0]
        queue.pop(0)
        self.__update_queue(queue, state)
        return Message.fromJSON(message)
    
    async def peek(self) -> Message:
        queue, _ = self.__get_queue()
        if queue.isEmpty():
            raise QueueEmpty(message="Queue is empty")
        message = queue[0]
        return Message.fromJSON(message)
    
    async def size(self) -> int:
        queue, _ = self.__get_queue()
        return len(queue)
    
    async def isEmpty(self) -> bool:
        queue, _ = self.__get_queue()
        return len(queue) == 0