#Rate Limiting - LLM API calls, web search calls, database queries, external tool calls
#BFS Agent Planning - agent explores possible actions level by level, deque helps
#Tool Call History - You may want to remember only the last 10 tool calls to avoid huge context.
#Agent Memory Buffer- remove oldest event, add newest event

# Core
#front = index of first element
#size = number of elements
#rear index = (front + size - 1) % capacity
#next rear insert index = (front + size) % capacity

class MyCircularDeque:

    def __init__(self, k: int):
        self.data = [None] * k
        self.capacity = k
        self.front = 0
        self.size = 0

    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False

        self.front = (self.front - 1) % self.capacity
        self.data[self.front] = value
        self.size += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull():
            return False

        rear_index = (self.front + self.size) % self.capacity
        self.data[rear_index] = value
        self.size += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False

        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty():
            return False

        rear_index = (self.front + self.size - 1) % self.capacity
        self.data[rear_index] = None
        self.size -= 1
        return True

    def getFront(self) -> int:
        if self.isEmpty():
            return -1

        return self.data[self.front]

    def getRear(self) -> int:
        if self.isEmpty():
            return -1

        rear_index = (self.front + self.size - 1) % self.capacity
        return self.data[rear_index]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity


class ShortTermMemory:
    def __init__(self, capacity: int):
        self.memory = MyCircularDeque(capacity)

    def add_memory(self, item: str) -> None:
        if self.memory.isFull():
            self.memory.deleteLast()   # remove oldest

        self.memory.insertFront(item)  # add newest

  
