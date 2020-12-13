# This code is credited to Glenn Liem
#
# Originally found in 
# https://github.com/gxavier38/CS511/blob/master/HW12/Question%205.py

from z3 import *
from itertools import combinations
from random import choice

n = 4
p = 1


# | |Q| | |
# | | | |R|
# |R| | | |
# | | |R| |

# n = 6
# p = 2


# | |R| | | | |
# | | | | |R| |
# | | | |R| | |
# | | | | | |Q|
# |Q| | | | | |
# | | |R| | | |

# n = 8
# p = 3

# | | | | | | | |R|
# | | |R| | | | | |
# | | | | | |R| | |
# | | | | |R| | | |
# | |Q| | | | | | |
# | | | |Q| | | | |
# |Q| | | | | | | |
# | | | | | | |R| |



def printMap(model):
    arr = [[" " for j in range(n)] for i in range(n)]
    for i in all_rows:
        for j in all_rows:
            if model[Q[i][j]] == True:
                arr[i][j] = "Q"
            elif model[R[i][j]] == True:
                arr[i][j] = "R" 
    res = ["|".join(x) for x in arr]
    res = ["|" + x + "|" for x in res]
    res = "\n".join(res)
    print(res)
    # res = "\033[4m" + res + "\033[4m"
    # print(res)

def difference(arr, elems):
    return list(set(arr) - set(elems))

s = Solver()

assert(p <= n)

# Choose random rows
all_rows = [i for i in range(n)]
rows = choice(list(combinations(all_rows, p)))
other_rows = difference(all_rows, rows)

# Variables
Q = [[Bool("Q" + str(i+1) + "," + str(j+1)) for j in range(n)] for i in range(n)]
R = [[Bool("R" + str(i+1) + "," + str(j+1)) for j in range(n)] for i in range(n)]

# Constraint 1
for i in rows:
    s.add(Or(Q[i]))

# Constraint 2
for i in other_rows:
    s.add(Or(R[i]))

# Constraint 3
for i in all_rows:
    for j in all_rows:
        s.add(Implies(Q[i][j], Not(R[i][j])))

# Constraint 4
for i in all_rows:
    for j in all_rows:
        s.add(Implies(Q[i][j], And([And(Not(Q[i][l]), Not(R[i][l])) for l in all_rows if l != j])))

# Constraint 5
for i in all_rows:
    for j in all_rows:
        s.add(Implies(Q[j][i], And([And(Not(Q[l][i]), Not(R[l][i])) for l in all_rows if l != j])))

# Constraint 6
for i in all_rows:
    for j in all_rows:
        s.add(Implies(R[i][j], And([And(Not(Q[i][l]), Not(R[i][l])) for l in all_rows if l != j])))

# Constraint 7
for i in all_rows:
    for j in all_rows:
        s.add(Implies(R[j][i], And([And(Not(Q[l][i]), Not(R[l][i])) for l in all_rows if l != j])))

# Constraint 8
for i in all_rows:
    for j in all_rows:
        s.add(Implies(Q[i][j], And([And(Not(Q[k][l]), Not(R[k][l])) for k in all_rows for l in all_rows if k != i and l != j and k - l == i - j])))

# Constraint 9
for i in all_rows:
    for j in all_rows:
        s.add(Implies(Q[i][j], And([And(Not(Q[k][l]), Not(R[k][l])) for k in all_rows for l in all_rows if k != i and l != j and k + l == i + j])))

if s.check() == unsat:
    print("Unsatisfiable!")
else:
    model = s.model()
    printMap(model)