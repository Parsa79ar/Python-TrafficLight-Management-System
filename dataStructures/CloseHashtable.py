class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self, size=10):        
        self.num_elements = 0
        self.data = [0] * size
        self.size = len(self.data)
        print(self.data)

    def __incrsize(self):
        self.size = self.size * 2
        tmplist = [0] * self.size
        for d in self.data:
            if d == 0:
                continue
            elif d == "deleted":
                continue
            else:
                i = 0
                while True:
                    hash_index = self.__get_hash_index(d.key, i)
                    if tmplist[hash_index] == 0:
                        tmplist[hash_index] = d
                        break
                    i += 1
        self.data = tmplist

    def __decrsize(self):
        if self.size / 2 >= 10:
            self.size = int(self.size / 2)
            tmplist = [0] * self.size
            for d in self.data:
                if d == 0:
                    continue
                elif d == "deleted":
                    continue
                else:
                    i = 0
                    while True:
                        hash_index = self.__get_hash_index(d.key, i)
                        if tmplist[hash_index] == 0:
                            tmplist[hash_index] = d
                            break
                        i += 1
            self.data = tmplist

    def __get_hash_index(self, key, i):
        return (key + i) % self.size


    def insert(self, key, value):
        i = 0
        hash_data = Node(key, value)
        while True:
            hash_index = self.__get_hash_index(key, i)
            if self.data[hash_index] == 0 or self.data[hash_index] == "deleted":
                self.data[hash_index] = hash_data
                break
            i += 1
        self.num_elements += 1
        if (self.num_elements / self.size) > (3/4):
            self.__incrsize()


    def get(self, key):
        i = 0
        while True:
            hash_index = self.__get_hash_index(key, i)
            if self.data[hash_index] != 0:
                if self.data[hash_index] == "deleted":
                    i += 1
                    continue
                if self.data[hash_index].key == key:
                    return self.data[hash_index]
                else:
                    i += 1
            elif self.data[hash_index] == 0:
                return


    def travers(self):
        for d in self.data:
            if d != 0:
                if d != "deleted":
                    yield d

    def remove(self, key):
        i = 0
        while True:
            hash_index = self.__get_hash_index(key, i)
            if self.data[hash_index] != 0:
                if self.data[hash_index] != "deleted":
                    if self.data[hash_index].key == key:
                        self.data[hash_index] = "deleted"
                        self.num_elements -= 1
                        if (self.num_elements / self.size) < (1/4):
                            self.__decrsize()
                        return
                i += 1
            elif self.data[hash_index] == 0:
                return "Hash key does not exist"