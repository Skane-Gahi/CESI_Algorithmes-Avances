# import numpy as np
# import pulp

# n_point = 10 # number of nodes
# k = 3
# distances = np.random.randint(low=0, high=1000, size=(n_point, n_point), dtype=np.uint)

# # set problem
# problem = pulp.LpProblem('cvrp_mip', pulp.LpMinimize)

# # set variables
# x = pulp.LpVariable.dicts('x', ((i, j) for i in range(n_point) for j in range(n_point)), lowBound=0, upBound=1, cat='Binary')

# # set objective function
# problem += pulp.lpSum([distances[i][j] * x[i, j] for i in range(n_point) for j in range(n_point)])

# # set constrains
# for i in range(n_point):
#     problem += x[i, i] == 0
    
# for i in range(1, n_point):
#     problem += pulp.lpSum(x[j, i] for j in range(n_point)) == 1
#     problem += pulp.lpSum(x[i, j] for j in range(n_point)) == 1
        
# problem += pulp.lpSum(x[i, 0] for i in range(n_point)) == k
# problem += pulp.lpSum(x[0, i] for i in range(n_point)) == k

# # solve problem
# status = problem.solve()

# # output status, value of objective function
# status, pulp.LpStatus[status], pulp.value(problem.objective)


adjacency = [[1,2,3,4,7,8,9,10,15], [4,5,9]]

def listEdgesColor(adjacency:list):
    succ, graphList = adjacency[0], []

    adjacency[1].insert(0,0)

    for truck in range(len(adjacency[1])-1):
        head = adjacency[1]
        circuit = succ[head[truck]:head[truck+1]]

        circuit.insert(0, 0)
        circuit.append(0)
        
        for city in range(len(circuit)-1):
            graphList.append((circuit[city], circuit[city+1], {"kamion": f"k{truck+1}"}))

    return graphList

print(listEdgesColor(adjacency))
