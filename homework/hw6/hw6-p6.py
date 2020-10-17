from z3 import *
fin = open('input.txt')
data = fin.readlines()
fin.close()
in_a = int(data[0])
m = int(data[1])
in_b = int(data[2])
n = int(data[3])

result = Bool('result')
out_A = [Int('out_a%s' % i) for i in range(m+1)]
out_B = [Int('out_b%s' % i) for i in range(n+1)]

phi_a = And(out_A[0] == in_a, And([out_A[i+1] == (out_A[i]*in_a) for i in range(m)]))
phi_b = And(out_B[0] == in_b, And([out_B[i+1] == (out_B[i]*out_B[i]) for i in range(n)]))

s = Solver()
Assumptions = And(phi_a, phi_b, in_a == in_b)

s.add(Not(Implies(Assumptions, out_A[m] == out_B[n])))

print(s.check())