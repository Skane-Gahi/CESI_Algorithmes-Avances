import networkx as nx 
import matplotlib.pyplot as plt

circuit = [[1,2,3,4,7,8,9,10,14,15,16,17,18], [4,8,13]]

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

G = nx.Graph()
G.add_edges_from(listEdgesColor(circuit))

# edge color
color_of_transport={'k1':'blue', 'k2':'orange', 'k3':'gold', 'k4':'green', 'k5':'red', 'k6':'purple', 'k7':'brown', 'k8':'pink', 'k9':'gray', 'k10':'cyan'}
transport_colors = [color_of_transport[prop['kamion']] for u, v, prop in G.edges(data=True)]

# Print graph into window
nx.draw_networkx(G, 
                node_color="red",
                edge_color=transport_colors,
                width=3)

plt.axis()
plt.show()

