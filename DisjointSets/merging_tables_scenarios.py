# python3

import sys

# n, m = map(int, sys.stdin.readline().split())
# lines = list(map(int, sys.stdin.readline().split()))

n, m = 10, 10
# n - the number of tables in the database and 
# m - the number of merge queries to perform

rows = [3, 5, 2, 0, 6, 10, 1, 13, 4, 2]
#  - the number of rows in each table for the table index

rank = [1] * n
parent = list(range(0, n))
ans = max(rows)

mergelist = [[0, 1], [1, 5], [4, 2], [1, 1], [10, 9], [8, 7], [10, 7], [6, 2], [3, 7], [5, 7]]

def getParent(table):
    # find parent and compress path
    return parent[table]

def merge(destination, source):
    realDestination, realSource = getParent(destination), getParent(source)

    if realDestination == realSource:
        return False

    # merge two components
    # use union by rank heuristic 
    # update ans with the new maximum table size
    
    return True

n, m = 10, 10
rows = [3, 5, 2, 0, 6, 10, 1, 13, 4, 2]
rank = [1] * n
parent = list(range(0, n))
ans = max(rows)

mergelist = [[0, 1], [1, 5], [4, 2], [1, 1], [0, 9], [8, 7], [0, 7], [6, 2], [3, 7], [5, 7]]

class TableInfo:
    
    def __init__(self, table_id, parent_id, nrows):
        self.table_id = table_id
        self.parent_id = parent_id
        self.nrows = nrows
        self.rank = 0
        
    def find(self, table_id, tables_list):
        if table_id != self.parent_id:
            return 
        else:
            self.parent_id = self.find(tables_list[table_id].parent_id, tables_list)
            return self.parent_id
 
# possible solution to compress path:
    # 1. find parent id of every table that is not parent itself
    # 2. add table ID that is not a parent_id to a list of table ids
    # 3. for each table id in a list, update it's parent id to the root parent
    #    with update_parent() function
    
    def find_root_id(self, table_id, tables_list):
        # finds parent table 
        # and compresses path to point to root parent table
        if table_id != self.parent_id:
            self.parent_id = self.find_root_id(self.parent_id, tables_list)
        #return tables_list[table_id].parent_id
        return self.parent_id
    
    def simple_merge(self, other, tables_list):
        # helper function
        tables_list[self.parent_id].nrows += tables_list[other.parent_id].nrows
        tables_list[other.parent_id].nrows = 0
        other.parent_id = self.parent_id
        return tables_list[self.parent_id].nrows
    
    def merge_ta(self, other, tables_list):
        root_self = tables_list[self.find_root_id(self.table_id, tables_list)]
        root_other = tables_list[other.find_root_id(other.table_id, tables_list)]
        
        print('self', root_self.parent_id, 'other', root_other.parent_id)

        
        if root_self.parent_id == root_other.parent_id:
            return root_self.nrows
        
        elif root_self.rank == root_other.rank:
            root_self.nrows += root_other.nrows
            root_other.nrows = 0
            root_other.parent_id = root_self.parent_id
            root_self.rank += 1
        
        elif root_self.rank < root_other.rank:
            root_other.nrows += root_self.nrows
            root_self.nrows = 0
            root_self.parent_id = root_other.parent_id
        else:
            # join other to self
            root_self.nrows += root_other.nrows
            root_other.nrows = 0
            root_other.parent_id = root_self.parent_id
        return max(root_self.nrows, 
                   root_other.nrows)
    
    def merge_sa(self, other, tables_list):
        # self.nrows = self.nrows + other.nrows
        print(self.parent_id, 'before merge')
        self.parent_id = self.find(other, tables_list)
        print(self.parent_id, 'self after merge')
        print(other.parent_id, 'other before merge')
        other.parent_id = self.parent_id
        print(other.parent_id, 'other after merge')
        
    def merge(self, other, tables_list):
        while (self.parent_id != self.table_id and
               other.parent_id != other.table_id):
            self = tables_list[self.parent_id]
            other = tables_list[other.parent_id]
        if self.parent_id == other.parent_id:
            pass
        elif self.rank == other.rank:
            tables_list[self.parent_id].nrows += tables_list[other.parent_id].nrows
            # clear the number of rows in old table, that now contains only symbolic link to parent table
            tables_list[other.parent_id].nrows = 0
            other.parent_id = self.parent_id
            self.rank += 1
        elif self.rank < other.rank:
            # join self to other
            # correct number of rows is stored in parent id
            tables_list[other.parent_id].nrows += tables_list[self.parent_id].nrows
            tables_list[self.parent_id].nrows = 0
            self.parent_id = other.parent_id
        else:
            # join other to self
            tables_list[self.parent_id].nrows += tables_list[other.parent_id].nrows
            tables_list[other.parent_id].nrows = 0
            other.parent_id = self.parent_id
        return max(tables_list[self.parent_id].nrows, 
                   tables_list[other.parent_id].nrows)



# does path compression work in find_parent_table?
m, n = 4, 5
parent = list(range(5))
rows = [1, 1, 1, 1, 1]
mergelist = [[3, 5], [4, 2], [4, 5], [4, 1]]
ans=1

tables_list = [TableInfo(table_id, parent_id, nrows)
              for table_id, parent_id, nrows in zip(parent, parent, rows)]

for i in range(m):
    # destination, source = map(int, sys.stdin.readline().split())

    source, destination = mergelist[i][0], mergelist[i][1]
    print(tables_list[source-1].find_root_id(source-1, tables_list),
          tables_list[destination-1].find_root_id(destination-1, tables_list))
    maxrows = tables_list[source-1].merge_ta(tables_list[destination-1], tables_list)
    ans = max(ans, maxrows)
    print(ans)
    print('', vars(tables_list[source-1]), '\n', vars(tables_list[destination-1]))









# random scenario
tables_list = [TableInfo(table_id, parent_id, nrows)
              for table_id, parent_id, nrows in zip(parent, parent, rows)]

for i, mlist in enumerate(mergelist):
    maxrows = tables_list[mlist[0]].merge(tables_list[mlist[1]], tables_list)
    ans = max(ans, maxrows)
    print(maxrows, ans)
    print(vars(tables_list[mlist[0]]), vars(tables_list[mlist[1]]))

print(tables_list[4].nrows)

print(vars(tables_list[mlist[0]]), vars(tables_list[mlist[1]]))


tables_list[0].merge(tables_list[1], tables_list)
print(vars(tables_list[0]), vars(tables_list[1]))
tables_list[0].merge(tables_list[2], tables_list)
print(vars(tables_list[0]), vars(tables_list[2]))
tables_list[0].merge(tables_list[4], tables_list)
print(vars(tables_list[0]), vars(tables_list[4]))


# example input
m, n = 4, 6
parent = list(range(6))
rows = [10, 0, 5, 0, 3, 3]
mergelist = [[5, 5], [5, 4], [4, 3], [3, 2]]
ans = 1

parent = list(range(5))
rows = [1, 1, 1, 1, 1]
mergelist = [[2, 4], [1, 3], [0, 3], [4, 3], [4, 2]]
ans=1


tables_list[0].find(0, tables_list)

cc = TableInfo(1, 1, 3)
print(cc)

vars(cc)
susu = [TableInfo(1, 1, 3)]


tables_list = [TableInfo(table_id, parent_id, nrows)
              for table_id, parent_id, nrows in zip(parent, parent, rows)]

# bad result:
    # I need to solve how the same table is joined to itself - how it changes the number of rows
m, n = 2, 2
rows = [2, 4]
rank = [1] * n
parent = parent = list(range(0, n))
mergelist = [[0, 0], [1, 1]]
ans = 3

tables_list[0].merge(tables_list[0], tables_list)
print(vars(tables_list[0]), vars(tables_list[1]))
tables_list[1].merge(tables_list[1], tables_list)
print(vars(tables_list[0]), vars(tables_list[1]))

# This scenario is OK, because merging the same tables doesn't change anything.

    # I need to solve how joining two disjoined sets referenced by bottom tables works
    # The reference should always be to the uppermost parent table and only that
    # one should contain number of rows of table. Other should have 0 rows.

for i in range(m):
    # destination, source = map(int, sys.stdin.readline().split())
    destination, source = mergelist[i][0], mergelist[i][1]
    maxrows = tables_list[source-1].merge(tables_list[destination-1], tables_list)
    ans = max(ans, maxrows)
    print(ans)
    

