class Node:
    def __init__(self, data = None):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert(data, self.root)

    def _insert(self, data, cur_node):
        if data < cur_node.data:
            if cur_node.left is None:
                cur_node.left = Node(data)
            else:
                self._insert(data, cur_node.left)
        elif data > cur_node.data:
            if cur_node.right is None:
                cur_node.right = Node(data)
            else:
                self._insert(data, cur_node.right)
        else:
            print("The value is already in tree...")
        
        # Balance Factor...
        balanceFactor = self.getBalance(cur_node)
        if balanceFactor > 1:
            if self.getBalance(cur_node.left) >= 0:
                return self.rightRotate(cur_node)
            else:
                cur_node.left = self.leftRotate(cur_node.left)
                return self.rightRotate(cur_node)
        if balanceFactor < -1:
            if self.getBalance(cur_node.right) <= 0:
                return self.leftRotate(cur_node)
            else:
                cur_node.right = self.rightRotate(cur_node.right)
                return self.leftRotate(cur_node)
        return cur_node

    def leftRotate(self, cur_node):
        y = cur_node.right
        T2 = y.left
        y.left = cur_node
        cur_node.right = T2
        cur_node.height = 1 + max(self.getHieght(cur_node.left), self.getHieght(cur_node.right))
        y.height = 1 + max(self.getHieght(y.left), self.getHieght(y.right))
        return y

    def rightRotate(self, cur_node):
        y = cur_node.left
        T3 = y.right
        y.right = cur_node
        cur_node.left = T3
        cur_node.height = 1 + max(self.getHieght(cur_node.left), self.getHieght(cur_node.right))
        y.height = 1 + max(self.getHieght(y.left), self.getHieght(y.right))
        return y

    # Get the height of the node
    def getHieght(self, cur_node):
        if cur_node is None:
            return 0
        return cur_node.height

    # Get balance factor of the node
    def getBalance(self, cur_node):
        if cur_node is None:
            return 0
        return self.getHieght(cur_node.left) - self.getHieght(cur_node.right)


avl = AVL()
nums = [13, 33, 45]
for num in nums:
    avl.insert(num)
    
print(avl.getBalance(13))
