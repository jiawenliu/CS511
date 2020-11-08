'''
This code is credited to Zongshun Zhang, originally found in 
https://github.com/Zongshun96/CS511/blob/master/hw8/
With the parse input file code rerwitten 
in order to adopt to the format provided in assignment 8
'''


import ast
from z3 import *
opt = Solver()
variable_d = {}
neg_var_d = {}


filename = sys.argv[1]
with open(filename, "r") as f:
    file = f.readlines()
w = eval(file[0])
c = eval(" ".join(file[1:]))


x_list = Ints(['x'+str(i) for i in range(len(w))])
not_x_list = Ints(['not_x'+str(i) for i in range(len(w))])

for i in range(len(w)):
    opt.add(Or(x_list[i] == 0, x_list[i] == 1))
    opt.add(Or(not_x_list[i] == 0, not_x_list[i] == 1))
    opt.add(Not(not_x_list[i] == x_list[i]))

exp = 0
# weight of S
for i in range(len(w)):
    exp = exp + w[i]*x_list[i]

# capacity of edge in S
temp = 0
for i in range(len(c)):
    for j in range(len(c[i])):
        temp = temp + c[i][j]*x_list[i]*x_list[j]

# if there are edges in S, penalize the weight.
exp = exp - (1+max(w))*temp



# Objective function
obj = Int("obj")
opt.add(obj == exp)

# Solve
if opt.check() == unsat:
	print("Unsatisfiable!")
	quit()
while opt.check() == sat:
	model = opt.model()
	opt.add(obj > model[obj])
print(model)