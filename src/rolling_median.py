import math
from heapq import heappush, heappop, heapify
'''
Below is a simple implementation of a rolling median calculationusing max heap and min heap.
Methods: add(int), push_max()
Additional functionality includes:
1) get_median()
2) variable called total which keeps track of the sum of all values
3) variable called size which keeps track of the total number of values
'''


class RollingMedian(object):
    
    def __init__(self):
        # initialize heaps, total, and size
        self.min_heap = []
        heapify(self.min_heap)
        self.max_heap = []
        heapify(self.max_heap)
        self.total = 0
        self.size = 0
    
    
    def add(self, val):
        self.size += 1
        self.total += val
        
        if not (len(self.max_heap) or len(self.min_heap)):
            self.push_max(val)
        elif len(self.max_heap) == 1 and not len(self.min_heap) :
            if val > self.top_max():
                self.push_min(val)
            else:
                x = self.pop_max()
                self.push_max(val)
                self.push_min(x)
        else:
            if val < self.top_max():
                self.push_max(val)
            else:
                self.push_min(val)
            
            # balance the heaps
            if len(self.max_heap) > len(self.min_heap):
                x = self.pop_max()
                self.push_min(x)
            
            if len(self.max_heap) < len(self.min_heap):
                x = self.pop_min()
                self.push_max(x)


    def get_median(self):
        median = 0
        
        if len(self.max_heap) == 0 and len(self.min_heap) == 0:
            return

        if len(self.max_heap) > len(self.min_heap):
            median = self.top_max()
        elif len(self.max_heap) < len(self.min_heap):
            median = self.top_min()
        else:
            median = (self.top_max() + self.top_min()) / 2

        fract, dec = math.modf(median)
        # round the median
        if fract < 0.5:
            median = dec
        else:
            median = dec + 1
        return int(median)

    # helper methods
    def push_max(self, val):
        heappush(self.max_heap, float(-1 * val))


    def push_min(self,val):
        heappush(self.min_heap, float(val))
    
    
    def pop_max(self):
        x = self.top_max()
        heappop(self.max_heap)
        return x
    
    
    def pop_min(self):
        x = self.top_min()
        heappop(self.min_heap)
        return x
    
    
    def top_max(self):
        return -1 * self.max_heap[0]
    
    
    def top_min(self):
        return self.min_heap[0]

