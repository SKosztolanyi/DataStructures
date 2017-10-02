# python3

import sys

n, m = map(int, sys.stdin.readline().split())
lines = list(map(int, sys.stdin.readline().split()))

rank = [0] * n
parent = list(range(0, n))
ans = max(lines)

class DisjointSet:
    
    def __init__(self, lines, n):
        self.nrows = lines
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, p):
        self.validate(p)
        if p != self.parent[p]:
            self.parent[p] = self.find(self.parent[p]) # path compression
        return self.parent[p]

    def connected(self, p, q):
        return self.find(p) == self.find(q)
		
    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ:
            return self.nrows[rootQ]
        
		# make root of smaller rank point to root of larger rank
        if self.rank[rootP] < self.rank[rootQ]:
            self.parent[rootP] = rootQ
            self.nrows[rootQ] += self.nrows[rootP]
            self.nrows[rootP] = 0
            
        elif self.rank[rootP] > self.rank[rootQ]:
            self.parent[rootQ] = rootP
            self.nrows[rootP] += self.nrows[rootQ]
            self.nrows[rootQ] = 0
        else:
            self.parent[rootQ] = rootP
            self.rank[rootP] += 1
            self.nrows[rootP] += self.nrows[rootQ]
            self.nrows[rootQ] = 0
        return max(self.nrows[rootQ], self.nrows[rootP])
    
    def validate(self, p):
        n = len(self.parent)
        if p < 0 or p >= n:
            raise IndexError("index {} is not between 0 and {}".format(p, n - 1)) 

ds = DisjointSet(lines, n)

for i in range(m):
    destination, source = map(int, sys.stdin.readline().split())
    maxrows = ds.union(source-1, destination-1)
    ans = max(ans, maxrows)
    print(ans)