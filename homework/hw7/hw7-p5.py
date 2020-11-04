"""
This solution is credited to Glenn Liem, originally found in
https://github.com/gxavier38/CS511/blob/master/HW7/Question%205.py
run the code withe the command: 
python hw7-p5.py [inputfilename]
for example: python hw7-p5.py input.txt
"""

from z3 import *

filename = sys.argv[1]

with open(filename, "r") as f:
    funcs = eval(" ".join(f.read().splitlines()))
num_funcs = len(funcs)
assert(num_funcs > 1)

variables = {}
num_vars = 0

# Parse the function at line i
def parse_function(i):
	current_func = funcs[i]
	tempfunc = 0

	# Parse terms of inequality
	for i in range(len(current_func)):
		current_term = current_func[i]
		coeff = current_term[0]
		tempterm = coeff

		# Parse variables of term
		for j in range(len(current_term[1])):
			varnum = current_term[1][j][1]

			# Construct variable if it doesn't exist
			if varnum not in variables:
				variables[varnum] = Int("x" + str(varnum))

			# Add term to inequality
			if current_term[1][j][0] == 1:
				tempterm = tempterm * (-variables[varnum])
			else:
				tempterm = tempterm * variables[varnum]

		tempfunc = tempfunc + tempterm
	return tempfunc

s = Solver()

# Constraints
for i in range(1, num_funcs):
	func = parse_function(i)
	print(func <= 0)
	s.add(func <= 0)

# Force variables to be 0 or 1
for i in variables:
	s.add(Or(variables[i] == 0, variables[i] == 1))

# Objective function
obj = Int("obj")
s.add(obj == parse_function(0))

# Solve
if s.check() == unsat:
	print("Unsatisfiable!")
	quit()
while s.check() == sat:
	model = s.model()
	s.add(obj < model[obj])
print(model)
