class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class MinHeap:
    def __init__(self, capacity=5):
        self.storage = [None] * capacity
        self.capacity = capacity
        self.size = 0

    def swap(self, index1, index2):
        temp = self.storage[index1]
        self.storage[index1] = self.storage[index2]
        self.storage[index2] = temp

    def insert(self, key, value):
        newNode = Node(key, value)
        if self.size == self.capacity:
            self.size = 0
            self.__incrcapacity()
        self.storage[self.size] = newNode
        self.size += 1
        self.heapifyUp(self.size - 1)
        

    def heapifyUp(self, index):
        if self.__getParentIndex(index) >= 0 and self.storage[self.__getParentIndex(index)].key > self.storage[index].key:
            self.swap(self.__getParentIndex(index), index)
            self.heapifyUp(self.__getParentIndex(index))
        print("--------up--------")
        print(self.storage)

    def removeMin(self):
        if self.size == 0:
            raise "Empty Heap"
        data = self.storage[0] 
        self.storage[0] = self.storage[self.size - 1]
        self.storage[self.size - 1] = None
        self.size -= 1
        self.heapifyDown(0)
        if (self.size / self.capacity) < (1/2):
            self.size = 0
            self.__decrcapacity()
        return data
    
    def heapifyDown(self, index):
        smallest = index
        if (self.__getLeftChildIndex(index) < self.size) and (self.storage[smallest].key > self.storage[self.__getLeftChildIndex(index)].key):
            smallest = self.__getLeftChildIndex(index)
        if (self.__getRightChildIndex(index) < self.size) and (self.storage[smallest].key > self.storage[self.__getRightChildIndex(index)].key):
            smallest = self.__getRightChildIndex(index)
        if smallest != index:
            self.swap(index, smallest)
            self.heapifyDown(smallest)
        print("----------down-------")
        print(self.storage)

    def __incrcapacity(self):
        tmplist = []
        for d in self.storage:
            tmplist.append(d)
        print("________inc_______")
        print(tmplist)
        
        self.capacity = self.capacity * 2
        self.storage = [None] * self.capacity
        for elm in tmplist:
            if elm:
                self.insert(elm.key, elm.value)

    def __decrcapacity(self):
        tmplist = []
        for d in self.storage:
            tmplist.append(d)
        print("________dec_______")
        print(tmplist)
        
        self.capacity = int(self.capacity / 2)
        self.storage = [None] * self.capacity
        for elm in tmplist:
            if elm:
                self.insert(elm.key, elm.value)

    def __getParentIndex(self, index):
        return (index - 1) // 2

    def __getLeftChildIndex(self, index):
        return 2 * index + 1

    def __getRightChildIndex(self, index):
        return 2 * index + 2