from z3 import *

graph = [
	(1, 2, [2, 3, 4, 5]),
	(2, 4, [1, 4]),
	(3, 4, [1, 5]),
	(4, 7, [1, 2, 5]),
	(5, 7, [1, 3, 4])
]

# Parse graph and add nodes
numNodes = len(graph)
weights = [0 for i in range(numNodes)]
adjacencyMatrix = [[0 for i in range(numNodes)] for j in range(numNodes)]

s = Solver()

nodes = []
letter = ord('a')

for i in range(numNodes):
	nodes.append(Int(chr(letter)))
	letter += 1

	weights[i] = graph[i][1]

	for j in graph[i][2]:
		adjacencyMatrix[i][j-1] = 1

# Check that graph is valid
for i in range(numNodes):
	if adjacencyMatrix[i][i] == 1:
		print("Self loop detected!")
		quit()

# Set nodes to either be 0 or 1
for i in range(numNodes):
	s.add(Or(nodes[i] == 0, nodes[i] == 1))

# Add weights
total = Int("total")
formula = 0
for i in range(numNodes):
	formula = weights[i] * nodes[i] + formula
s.add(total == formula)
s.add(total > 0)

# Add constraints that clique is connected
for i in range(numNodes):
	for j in range(i+1, numNodes):
		s.add(Or(nodes[i] * nodes[j] == 0, adjacencyMatrix[i][j] == 1))

# Search for clique with maximum weight
if (s.check() == unsat):
	print("No valid clique found!")
	quit()

while s.check() == sat:
	model = s.model()
	s.add(total > model[total])
print(model)