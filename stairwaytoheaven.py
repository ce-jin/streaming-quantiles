import numpy as np
import bisect
from math import inf

class StairwayToHeaven:
    def __init__(self, max_size:int, max_inf = inf, min_inf = -inf):
        self.max_height = 0
        self.max_size = max_size
        self.n = 0
        self.x_min = max_inf 
        self.x_max = min_inf 
        self.items = [[self.x_max,self.x_min,0,0,0]] #[x1,x2,y1,y2, number_of_times]
        self.freq = [0 for i in range(max_size+1)]

    def update(self, x):
        self.x_max = max(self.x_max, x)
        self.x_min = min(self.x_min, x)
        
        self.n += 1                   
        i = bisect.bisect_left([item[0] for item in self.items], x) # TODO
        self.items.insert(i, self.items[i-1].copy())
        self.items[i-1][1] = x
        self.items[i][0] = x
        for item in self.items[i:]:
            item[2]+=1
            item[3]+=1

        if len(self.items) > self.max_size:
            deleted_box_index = self.sqweeze()
            return deleted_box_index
           
    def sqweeze(self):
        best_h = inf
        best_i = None
        for i in range(len(self.items)-1):
            h = self.items[i+1][3]-self.items[i][2]
            if h < best_h:
                best_h = h
                best_i = i
        self.items[best_i][1] = self.items[best_i+1][1]
        self.items[best_i][3] = self.items[best_i+1][3]
        #print(self.get_freq())
        #print(best_i)
        self.items[best_i][4] += self.items[best_i+1][4] + 1
        self.items.pop(best_i+1)
        #print(self.get_freq())
        self.freq[best_i] += 1
        return best_i+1
        
    def get_bounds(self):
        x1s,x2s,y1s,y2s = (np.array(l) for l in list(zip(*self.items)))
        x1s[0] = self.x_min
        x2s[-1] = self.x_max
        return x1s, x2s, y1s, y2s

    def max_error_range(self):
        i = np.argmax([item[3]-item[2] for item in self.items])
        x1 = self.items[i][0]
        x2 = self.items[i][1]
        return x1,x2
    
    def get_error(self):
        return max([item[3]-item[2] for item in self.items])
    
    def get_heights(self):
        return [item[3]-item[2] for item in self.items]

    def get_freq(self):
        #return [item[4] for item in self.items]
        return self.freq

    def get_memory(self):
        mem = set()
        for item in self.items:
            mem.add(item[0])
            mem.add(item[1])
        return list(mem)