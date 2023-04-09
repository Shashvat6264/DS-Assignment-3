from .LockedQueue import LockedQueue
from .Message import Message
from .RaftAdapter import RaftAdapter
from .RaftQueue import RaftQueue

from ..models import *

class Partition:
    def __init__(self, partition_id: int, topic_name: str, raft_server = None, database = None):
        self.__id = partition_id
        self.__topic = topic_name
        self.__database = database
        if raft_server is not None:
            self.__raftAdapter = RaftAdapter(raft_server, self)
            self.__queue = RaftQueue(self.__raftAdapter)
        else:
            self.__raftAdapter = None
            self.__queue = None
    
    def init_partition(self):
        self.__raftAdapter.update_state({
            'queue': [],
            'consumerOffsets': {}
        })
        
    def update_raft_server(self, raft_server):
        self.__raftAdapter.set_raft_server(raft_server)
    
    def __get_consumerOffsets(self):
        state = self.__raftAdapter.get_state()
        if state is not None:
            return state['consumerOffsets'], state
        else:
            return {}, state
        
    def __update_consumerOffsets(self, offsets, state = None):
        if state is None:
            state = self.__raftAdapter.get_state()
            if state is None:
                return
        state['consumerOffsets'] = offsets
        self.__raftAdapter.update_state(state)
        
    def getId(self) -> int:
        return self.__id
    
    def getTopic(self) -> str:
        return self.__topic
    
    async def save(self):
        if self.__database is not None:
            await self.__database.create(PartitionModel, id=self.__id, topicname=self.__topic)
    
    async def pushMessage(self, id: int, message: Message):
        index = await self.__queue.push(message)
        if self.__database is not None:
            partitionInstance = self.__database.getById(PartitionModel, self.__id)
            messageInstance = self.__database.getById(MessageModel, message.getId())
            partitionInstance.messages.append(messageInstance)
            messageInstance.index = index
            messageInstance.partition_id = partitionInstance.id
            await self.__database.updateById(MessageModel, message.getId(), index=messageInstance.index, partition_id=messageInstance.partition_id)
            await self.__database.updateById(PartitionModel, self.__id, messages=partitionInstance.messages)
        
    async def popMessage(self, id: int) -> Message:
        consumerOffsets, state = self.__get_consumerOffsets()
        if consumerOffsets.get(str(id)) is None:
            consumerOffsets[str(id)] = 0
        
            if self.__database is not None:
                consumerInstance = await self.__database.create(ConsumerModel, pid=id, offset=0, partition_id=self.__id)
                partitionInstance = self.__database.getById(PartitionModel, self.__id)
                partitionInstance.consumers.append(consumerInstance)
                await self.__database.updateById(PartitionModel, self.__id, consumers=partitionInstance.consumers)
        
        message = await self.__queue.getIndex(consumerOffsets[str(id)])
        consumerOffsets[str(id)] += 1
        
        if self.__database is not None:
            partitionInstance = self.__database.getById(PartitionModel, self.__id)
            for consumerInstance in partitionInstance.consumers:
                if consumerInstance.pid == id:
                    await self.__database.updateById(ConsumerModel, consumerInstance.id, offset=consumerInstance.offset+1)
                    break
        
        self.__update_consumerOffsets(consumerOffsets, state)
        return message
        
    async def getSize(self, id: int) -> int:
        consumerOffsets, _ = self.__get_consumerOffsets()
        if consumerOffsets.get(str(id)) is None:
            consumerOffsets[str(id)] = 0
            
            if self.__database is not None:
                consumerInstance = await self.__database.create(ConsumerModel, pid=id, offset=0, partition_id=self.__id)
                partitionInstance = self.__database.getById(PartitionModel, self.__id)
                partitionInstance.consumers.append(consumerInstance)
                await self.__database.updateById(PartitionModel, self.__id, consumers=partitionInstance.consumers)
                
        total_size = await self.__queue.size()
        return total_size - consumerOffsets[str(id)]
    
    def modelToObj(instance, database, raft_process):
        partition = Partition(partition_id=instance.id, topic_name=instance.topicname, database=database, raft_server=raft_process)
        sorted(instance.messages, key=lambda x: x.index)
        
        messageList = []
        for messageInstance in instance.messages:
            message = Message.modelToObj(messageInstance)
            messageList.append(message)
        
        consumerOffsets = {}
        for consumerInstance in instance.consumers:
            consumerOffsets[consumerInstance.pid] = consumerInstance.offset
            
        #TODO-> Only to do if no other entry already present in raft
        partition.__raftAdapter.update_state({
            'queue': messageList,
            'consumerOffsets': consumerOffsets
        })
        
        return partition