from z3 import *
    
s = Solver()

ina0, outa0, outa1, outa2, inb0, outb0 = Ints('ina0 outa0 outa1 outa2 inb0 outb0')

phia = And((outa0 == ina0), (outa1 == outa0*ina0), (outa2 == outa1*ina0))
phib = (outb0 == (inb0*inb0)*inb0)

psi = Implies(And((ina0 == inb0), phia, phib), (outa2 == outb0))

s.add(Not(psi))
print(s.check())