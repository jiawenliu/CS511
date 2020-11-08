'''
This code is credited to Zongshun Zhang, originally found in 
https://github.com/Zongshun96/CS511/blob/master/hw8/q6.py
With the parse input file code rerwitten 
in order to adopt to the format provided in assignment 8
'''


from z3 import *
import sys
import numpy as np
import ast
import json

filename = sys.argv[1]
with open(filename, "r") as f:
    file = f.readlines()
weight = eval(file[0])
capacity = eval(" ".join(file[1:]))

def main():
    s = Optimize()
    constraint = []
    function = objectiveFunction()
    constraints(constraint)
    s.add(constraint)
    s.maximize(function)
    if s.check() == sat:
        model = s.model()
        for a in model:
            if '-' not in str(a):
                print('variable: ' + str(a) + ' value = ' + str(model[a]))
    else:
        print('False, error to solve the problem!')

def objectiveFunction():
    function = 0
    for i, lists in enumerate(capacity):
        for j, capacity_ij in enumerate(lists):
            if j >= i and capacity_ij > 0:
                function += capacity_ij * (Int('x_%s' % (i+1)) * Int('-x_%s' % (j+1)) + Int('-x_%s' % (i+1)) *
                            Int('x_%s' % (j+1)))
    return function

# setting up constraints: variables can only assume values 0 or 1, and the sum of x and Bar x is 1
def constraints(constraint):
    for i, x in enumerate(weight):
        constraint.append(Or(Int('x_' + str(i+1)) == 1, Int('x_' + str(i+1)) == 0))
        constraint.append(Or(Int('-x_' + str(i+1)) == 1, Int('-x_' + str(i+1)) == 0))
        constraint.append(Int('x_' + str(i+1)) + Int('-x_' + str(i+1)) == 1)


if __name__== "__main__":
    main()