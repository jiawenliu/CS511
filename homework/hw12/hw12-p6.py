'''
This code is credited to Zichen Zhu,
Originally found in :
https://github.com/littlepig2013/CS511-Formal-Method/blob/master/hw12/problem6.py
'''


from z3 import *
import sys, random, math, copy
def gen_subset(x,n):
    result = list(range(n))
    for j in range(x):
        i = random.randrange(j, n)
        tmp = result[j]
        result[j] = result[i]
        result[i] = tmp
    return result[:x], result[x:]


n = 8

Qs = [ [ Bool('q_%s_%s' % (i, j) ) for j in range  (n) ]  for i in range(n) ]
Rs = [ [ Bool('r_%s_%s' % (i, j) ) for j in range  (n) ]  for i in range(n) ]
P, Remain = gen_subset(int(math.ceil(n*1.0/3)),n) 
varphi_1 = And([Or([Qs[i][j] for j in range(n)]) for i in P])
varphi_2 = And([Or([Rs[i][j] for j in range(n)]) for i in Remain])
varphi_3 = And([And([Implies(Qs[i][j], Not(Rs[i][j])) for j in range(n)]) for i in range(n)])
varphi_4 = And([And([Implies(Qs[i][j], And([And(Not(Qs[i][l]),Not(Rs[i][l])) for l in [x for x in range(n) if x != j]])) for j in range(n)]) for i in range(n)])
varphi_5 = And([And([Implies(Qs[i][j], And([And(Not(Qs[k][j]),Not(Rs[k][j])) for k in [x for x in range(n) if x != i]])) for j in range(n)]) for i in range(n)])
varphi_6 = And([And([Implies(Rs[i][j], And([And(Not(Qs[i][l]),Not(Rs[i][l])) for l in [x for x in range(n) if x != j]])) for j in range(n)]) for i in range(n)])
varphi_7 = And([And([Implies(Rs[i][j], And([And(Not(Qs[k][j]),Not(Rs[k][j])) for k in [x for x in range(n) if x != i]])) for j in range(n)]) for i in range(n)])

varphi_8 = And([And([And([And([If(x - y == i - j and x != i, Implies(Qs[i][j], And(Not(Qs[x][y]),Not(Rs[x][y]))), True) for y in range(n)]) for x in range(n)]) for j in range(n)]) for i in range(n)])
varphi_9 = And([And([And([And([If(x + y == i + j and x != i, Implies(Qs[i][j], And(Not(Qs[x][y]),Not(Rs[x][y]))), True) for y in range(n)]) for x in range(n)]) for j in range(n)]) for i in range(n)])

total_varphi = [varphi_1, varphi_2, varphi_3, varphi_4, varphi_5, varphi_6, varphi_7, varphi_8, varphi_9]
total_varphi.reverse()

for i in range(9):
    s = Solver()
    result = total_varphi.pop()
    for v in total_varphi:
        s.add(v)
    s.add(Not(result))
    if s.check() == unsat:
        print "Constraint " + str(i+1) + " CAN be derived from the rest 8 wffs"
    else:
        print "Constraint " + str(i+1) + " CANNOT be derived from the rest 8 wffs"
    total_varphi.insert(0,result)
    #print len(total_varphi)