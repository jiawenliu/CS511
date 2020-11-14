# -*- coding: utf-8 -*-
"""
The code is credited to Zongping Zhang
Created on Fri Nov 13 20:02:16 2020
@author: ZZPzz
"""

from z3 import *
import json

"""Inputs"""

test = ""
if test=='testcase1':
    CPTs = [
            ["a",[[[["c","F"],["b","F"]],["a","F"],0.99], 
                  [[["c","F"],["b","F"]],["a","T"],0.01], 
                  [[["c","F"],["b","T"]],["a","F"],0.1],
                  [[["c","F"],["b","T"]],["a","T"],0.9],
                  [[["c","T"],["b","F"]],["a","F"],0.3],
                  [[["c","T"],["b","F"]],["a","T"],0.7], 
                  [[["c","T"],["b","T"]],["a","F"],0.01],
                  [[["c","T"],["b","T"]],["a","T"],0.99]]],
            ["b",[[[],["b","F"],0.7], [[],["b","T"],0.3]]],
            ["c",[[[],["c","F"],0.9], [[],["c","T"],0.1]]],
            ]
    
    Os = [['c','T']]
    
    # with open("q5_lists.txt","w") as f:
    #     json.dump([CPTs,Os],f)
        
else:
    CPTs = [
        ["V1", [[[], ["V1", "T"], 0.3], [[], ["V1", "F"], 0.7]]],
        ["V2", [[[], ["V2", "T"], 0.2], [[], ["V2", "F"], 0.8]]],
        ["V3", [[[], ["V3", "T"], 0.9], [[], ["V3", "F"], 0.1]]],
        ["V4", [[[["V1", "T"], ["V2", "T"]], ["V4", "T"], 0.2],
               [[["V1", "T"], ["V2", "T"]], ["V4", "F"], 0.8],
               [[["V1", "T"], ["V2", "F"]], ["V4", "T"], 0.9],
               [[["V1", "T"], ["V2", "F"]], ["V4", "F"], 0.1],
               [[["V1", "F"], ["V2", "T"]], ["V4", "T"], 0.1],
               [[["V1", "F"], ["V2", "T"]], ["V4", "F"], 0.9],
               [[["V1", "F"], ["V2", "F"]], ["V4", "T"], 0.4],
               [[["V1", "F"], ["V2", "F"]], ["V4", "F"], 0.4]]],
        ["V5", [[[["V2", "T"], ["V2", "T"]], ["V5", "T"], 0.5],
               [[["V2", "T"], ["V3", "T"]], ["V5", "F"], 0.5],
               [[["V2", "T"], ["V3", "F"]], ["V5", "T"], 0.6],
               [[["V2", "T"], ["V3", "F"]], ["V5", "F"], 0.4],
               [[["V2", "F"], ["V3", "T"]], ["V5", "T"], 0.3],
               [[["V2", "F"], ["V3", "T"]], ["V5", "F"], 0.7],
               [[["V2", "F"], ["V3", "F"]], ["V5", "T"], 0.1],
               [[["V2", "F"], ["V3", "F"]], ["V5", "F"], 0.9]]],
        ["V6", [[[["V5", "F"]], ["V6", "F"], 0.1],
               [[["V5", "F"]], ["V6", "T"], 0.9],
               [[["V5", "F"]], ["V6", "F"], 0.5],
               [[["V5", "F"]], ["V6", "T"], 0.5]]],
        ["V7", [[[["V4", "F"]], ["V7", "F"], 0.7],
               [[["V4", "F"]], ["V7", "T"], 0.3],
               [[["V4", "F"]], ["V7", "F"], 0.4],
               [[["V4", "F"]], ["V7", "T"], 0.6]]],     
        ["V8", [[[["V4", "T"], ["V5", "T"]], ["V8", "T"], 0.4],
               [[["V4", "T"], ["V5", "T"]], ["V8", "F"], 0.6],
               [[["V4", "T"], ["V5", "F"]], ["V8", "T"], 0.5],
               [[["V4", "T"], ["V5", "F"]], ["V8", "F"], 0.5],
               [[["V4", "F"], ["V5", "T"]], ["V8", "T"], 0.6],
               [[["V4", "F"], ["V5", "T"]], ["V8", "F"], 0.4],
               [[["V4", "F"], ["V5", "F"]], ["V8", "T"], 0.7],
               [[["V4", "F"], ["V5", "F"]], ["V8", "F"], 0.3]]]

    ]
    Os = [["V1", "T"]]

relationship_dict = {}
for CPT in CPTs:# CPT: [V,T], V: variable name (str) T: [[Cs, [V,v], p],...,[Cs,[V,v],p]]
    if CPT[0] not in relationship_dict:
        relationship_dict[CPT[0]] = []
    for conditions in CPT[1]:
        for C in conditions[0]:
            relationship_dict[CPT[0]].append(C[0])
        break
    
    
s = Solver()
variables_dict = {}

for var in relationship_dict:
    variables_dict[var] = (Int(var))
    
for var_name in variables_dict:
    s.add(Or(variables_dict[var_name]==0,variables_dict[var_name] == 1))

for observation in Os:
    var_name = observation[0]
    s.add(variables_dict[var_name]==1 if observation[1]=='T' else variables_dict[var_name]==0)


objective = 1.0

for CPT in CPTs:
    var = CPT[0]
    clause = 0
    if len(relationship_dict[var]) == 0: # no parents
        for pro in CPT[1]:
            if pro[1][1] == "T":
                true_prob = pro[2]*100.0
            else:
                false_prob = pro[2]*100.0
        clause = variables_dict[var]*true_prob + (1-variables_dict[var])*false_prob 
        
    else:
        for condition in CPT[1]:
            term = 1
            for vari in condition[0]:
                if vari[1] == "T":
                    term = term * variables_dict[vari[0]]
                else:
                    term = term * (1 - variables_dict[vari[0]])
            term = term * (condition[2] * 100.0) * (variables_dict[var] if condition[1][1]=="T" else (1-variables_dict[var]))
            clause += term;

    objective = objective * clause # CNF


obj = Int("obj")
s.add(obj == objective)
if s.check() == unsat:
    print("Unsatisfiable!")
    quit()
while s.check() == sat:
    model = s.model()
    s.add(obj > model[obj])
print(model)