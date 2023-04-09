from .Message import Message
from .Partition import Partition
from .exceptions import *

from ..models import *

class DistributedQueue:
    def __init__(self, database = None, raft_process = None):
        self.__database = database
        self.__partitions = {}
        self.__raft_process = raft_process
        
    def set_raft_process(self, raft_process):
        self.__raft_process = raft_process
        
    def loadPersistence(self):
        if self.__database is not None:
            partitionList = self.__database.read(PartitionModel)
            for partitionInstance in partitionList:
                self.__partitions[partitionInstance.id] = Partition.modelToObj(partitionInstance, self.__database, self.__raft_process)
    
    def getPartitions(self) -> list:
        return list(self.__partitions.values())
    
    async def connect_broker(self, config, address):
        self.__raft_process = await self.__raft_process.addNode(config, address)
        for partition in list(self.__partitions.values()):
            partition.update_raft_server(self.__raft_process)
    
    async def createPartition(self, topic_name: str, partition_id: int):
        if partition_id in self.__partitions.keys():
            raise PartitionAlreadyExists("Partition of id: {partition_id} already exists")
        partition = Partition(partition_id, topic_name, self.__raft_process, self.__database)
        partition.init_partition()
        self.__partitions[partition_id] = partition
        await partition.save()
    
    async def enqueue(self, partition_id: int, id: int, message: str):
        if self.__partitions.get(partition_id) is None:
            raise PartitionDoesNotExist("Partition id: {partition_id} does not exist")
        msg = Message(message)
        await msg.save(self.__database)
        await self.__partitions[partition_id].pushMessage(id, msg)
        
    async def dequeue(self, partition_id: int, id: int) -> str:
        if self.__partitions.get(partition_id) is None:
            raise PartitionDoesNotExist("Partition id: {partition_id} does not exist")
        message = await self.__partitions[partition_id].popMessage(id)
        return message.getMessage()
    
    async def size(self, partition_id: int, id: int) -> int:
        if self.__partitions.get(partition_id) is None:
            raise PartitionDoesNotExist("Partition id: {partition_id} does not exist")
        return await self.__partitions[partition_id].getSize(id)
        
    
    