import math

'''
Below is a simple implementation of a Red-Black Tree ADT.
The RBT helps to keep track of running median.
The self-balancing nature of the tree allows for the following:
    * if the number of nodes in left and right subtrees
    relative to the root are equal, the median is the root
    * if the number of nodes in left subtree is greater, then the median is
    the average of the root and root.left node value
    * if the number of nodes in right subtree is greater, then the median is
    the average of the root and root.right node value
Delete is not implemented because it is unnecessary for keeping track of median.
Additional functionality includes:
1) get_median()
2) variable called total which keeps track of the sum of all node values
'''

class RedBlackTree:
    def __init__(self):
        self.root = NilNode.instance()
        self.size = 0
        self.num_right_nodes = 0
        self.num_left_nodes = 0
        self.total = 0
    
    def __str__(self):
        print_tree = "Size of tree is {0}\nNumber left nodes: {1}\nNumber right nodes: {2}\n".format(self.size, self.num_left_nodes, self.num_right_nodes)
        return print_tree

    def add(self, value):
        self.insert(Node(value))
    
    def get_median(self):
        median = 0
        fract = 0
        dec = 0
        size = 1 + self.num_left_nodes + self.num_right_nodes
        if size == 1:
            median = self.root.value
            fract, dec = math.modf(median)
        elif self.num_right_nodes < self.num_left_nodes:
            median = (self.root.value + self.root.left.value) / 2
            fract, dec = math.modf(median)

        elif self.num_right_nodes > self.num_left_nodes:
            median = (self.root.value + self.root.right.value) / 2
            fract, dec = math.modf(median)
        elif self.num_right_nodes == self.num_left_nodes:
            median = self.root.value
            fract, dec = math.modf(median)
            
        if fract < 0.5:
            median = dec
        else:
            median = dec + 1
        return int(median)
    
    def insert(self, x):
        self.size += 1
        self.total += x.value

        if self.size % 2 == 1:
            self.num_left_nodes = self.size // 2
            self.num_right_nodes = self.num_left_nodes 
        else:       
            if self.size > 0:
                if x.value < self.root.value:
                    self.num_left_nodes += 1
                elif x.value >= self.root.value:
                    self.num_right_nodes += 1
                
        self.__insert_helper(x)

        x.color = Node.RED
        while x != self.root and x.parent.color == Node.RED:
            if x.parent == x.parent.parent.left:
                y = x.parent.parent.right
                if y and y.color == Node.RED:
                    x.parent.color = Node.BLACK
                    y.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    x = x.parent.parent
                else:
                    if x == x.parent.right:
                        x = x.parent
                        self.__left_rotate(x)
                    x.parent.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    self.__right_rotate(x.parent.parent)
            else:
                y = x.parent.parent.left
                if y and y.color == Node.RED:
                    x.parent.color = Node.BLACK
                    y.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    x = x.parent.parent
                else:
                    if x == x.parent.left:
                        x = x.parent
                        self.__right_rotate(x)
                    x.parent.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    self.__left_rotate(x.parent.parent)
        self.root.color = Node.BLACK


    def successor(self, x):
        if x.right:
            return self.minimum(x.right)
        y = x.parent
        while y and x == y.right:
            x = y
            y = y.parent
        return y

    def inorder_walk(self, x = None):
        if x is None: x = self.root
        x = self.minimum()
        while x:
            yield x.value
            x = self.successor(x)

    def search(self, value, x = None):
        if x is None: x = self.root
        while x and x.value != value:
            if value < x.value:
                x = x.left
            else:
                x = x.right
        return x

    def is_empty(self):
        return bool(self.root)

    def __left_rotate(self, x):
        if not x.right:
            raise "x.right is nil!"
        y = x.right
        x.right = y.left
        if y.left: y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def __right_rotate(self, x):
        if not x.left:
            raise "x.left is nil!"
        y = x.left
        x.left = y.right
        if y.right: y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y

    def __insert_helper(self, z):
        y = NilNode.instance()
        x = self.root
        while x:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        
        z.parent = y
        if not y:
            self.root = z
        else:
            if z.value < y.value:
                y.left = z
            else:
                y.right = z


class Node:
    RED = True
    BLACK = False
    
    def __init__(self, value, color = RED):
        if not type(color) == bool:
            raise TypeError("Expected True/False!")
        self.color = color
        self.value = value
        self.left = self.right = self.parent = NilNode.instance()
    
    def __str__(self, level = 0, indent = '\t'):
        s = level * indent + str(self.value)
        if self.left:
            s = s + '\n' + self.left.__str__(level + 1, indent)
        if self.right:
            s = s + '\n' + self.right.__str__(level + 1, indent)
        return s
    
    def __nonzero__(self):
        return True
    
    def __bool__(self):
        return True


class NilNode(Node):
    __instance__ = None
    
    @classmethod
    def instance(self):
        if self.__instance__ is None:
            self.__instance__ = NilNode()
        return self.__instance__
    
    def __init__(self):
        self.color = Node.BLACK
        self.value = None
        self.left = self.right = self.parent = None
    
    def __nonzero__(self):
        return False
    
    def __bool__(self):
        return False



