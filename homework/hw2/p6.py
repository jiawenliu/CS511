from z3 import *

p1, p2, p3, p4 = Bools('p1 p2 p3 p4')
# parity CNF
phi = And(Or(Not(p1), p2, p3, p4),Or(p1, Not(p2), p3, p4),Or(p1, p2, Not(p3), p4),Or(p1, p2, p3, Not(p4)),Or(Not(p1), Not(p2), Not(p3), p4),Or(Not(p1), p2, Not(p3), Not(p4)),Or(Not(p1), Not(p2), p3, Not(p4)),Or(p1, Not(p2), Not(p3), Not(p4)))
# parity DNF
psi = Or(And(Not(p1),Not(p2),Not(p3),Not(p4)),And(p1,p2,p3,p4),And(Not(p1),Not(p2),p3,p4),And(Not(p1),p2,Not(p3),p4),And(Not(p1),p2,p3,Not(p4)),And(p1,Not(p2),Not(p3),p4),And(p1,Not(p2),p3,Not(p4)),And(p1,p2,Not(p3),Not(p4)),)

def biconditional(p1, p2):
	return And(Implies(p1, p2), Implies(p2, p1))
# parity biconditional
theta = biconditional(biconditional(biconditional(p1, p2), p3), p4)
s1 = Solver()
s1.add(phi != psi)
print s1.check()
s2 = Solver()
s2.add(psi != theta)
print s2.check()
