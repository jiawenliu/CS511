# -*- coding: utf-8 -*-
"""
The code is credited to Zichen Zhu
Originally found in:
https://github.com/littlepig2013/CS511-Formal-Method/blob/master/hw10/network-builder.py
However, this code is not completely correct. 
The resulting graph should be a tree by running the MaxSAT incrementally. 
While this code runs the MaxSAT only once, resulting a forest instead of a tree.
"""

import ast
from z3 import *
# parsing data by replacing the inputs with corresponding test cases
(m,n) = (6,10)
PierP = [(1,1),(2,7),(3,3),(3,8),(6,8)]
BlockedP = [(2,3),(2,5),(2,8),(4,4),(4,5),(4,9),(5,5),(6,1)]



Q = [ [Bool('q_%s_%s' % (i, j)) for j in range(n)] for i in range(m)]

s = Optimize()
occupiedP = set()
# C1
for i, j in PierP:
  s.add(Q[i-1][j-1])
  occupiedP.add((i-1,j-1))
# C2
for i, j in BlockedP:
  s.add(Not(Q[i-1][j-1]))
  occupiedP.add((i-1,j-1))

# C3
def adj(i, j):
  results = set()
  row_min_bound = max(i-1, 0)
  row_max_bound = min(i+1, m-1) 
  col_min_bound = max(j-1, 0)
  col_max_bound = min(j+1, n-1) 
  for x in range(row_min_bound, row_max_bound+1):
    if x != i:
      results.add((x, j))
  for y in range(col_min_bound, col_max_bound+1):
    if y != j:
      results.add((i, y))
  return results

for i, j in PierP:
  adjP = adj(i-1, j-1)
  s.add(Or([Q[x][y] for x,y in adjP]))
  s.add(And([Implies(Q[x][y], And([Not(Q[xt][yt]) for xt, yt in adjP - {(x,y)}])) for x, y in adjP]))

s.add(Or([Q[x][y] for x,y in adj(i-1,j-1) - occupiedP for i, j in PierP]))

# C4

for i in range(m):
  for j in range(n):
    if (i,j) not in occupiedP:
      adjP = adj(i,j)
      s.add(Implies(Q[i][j], Or([Or([And(Q[xt][yt],Q[x][y]) for xt, yt in adjP - {(x,y)}]) for x,y in adjP])))

s.maximize(sum([sum([ If(Not(Q[i][j]), 1, 0)  for j in range(n)]) for i in range(m)]))
if s.check() == sat:
  model = s.model()
  results = []
  for i in range(m):
    for j in range(n):
      if model.evaluate(Q[i][j]) and (i,j) not in occupiedP:
        results.append((i+1,j+1))
  print(results)
else:
  print("unsat")
