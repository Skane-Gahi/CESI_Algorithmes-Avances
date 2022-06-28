import numpy as np
import pulp

v = 10 # number of nodes
k = 3
A = np.random.randint(low=0, high=1000, size=(v, v), dtype=np.uint)

# set problem
problem = pulp.LpProblem('cvrp_mip', pulp.LpMinimize)

# set variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(v) for j in range(v)), lowBound=0, upBound=1, cat='Binary')

# set objective function
problem += pulp.lpSum([A[i][j] * x[i, j] for i in range(v) for j in range(v)])

# set constrains
for i in range(v):
    problem += x[i, i] == 0
    
for i in range(1, v):
    problem += pulp.lpSum(x[j, i] for j in range(v)) == 1
    problem += pulp.lpSum(x[i, j] for j in range(v)) == 1
        
problem += pulp.lpSum(x[i, 0] for i in range(v)) == k
problem += pulp.lpSum(x[0, i] for i in range(v)) == k

# solve problem
status = problem.solve()

# output status, value of objective function
status, pulp.LpStatus[status], pulp.value(problem.objective)