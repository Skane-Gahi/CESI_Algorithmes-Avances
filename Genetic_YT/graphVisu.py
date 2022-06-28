import networkx as nx 
import matplotlib.pyplot as plt

# circuit = [[1,2,3,4,7,8,9,10,14,15,16,17,18], [4,8,13]]

def listEdgesColor(adjacency:list):
    adjacency[1].sort()
    # print(adjacency[1])
    succ, graphList = adjacency[0], []
    adjacency[1].insert(0,0)
    head = adjacency[1]

    for truck in range(len(adjacency[1])-1):
        circuit = succ[head[truck]:head[truck+1]]
        circuit.insert(0, 0)
        circuit.append(0)
        for city in range(len(circuit)-1):
            graphList.append((circuit[city], circuit[city+1], {"kamion": f"k{truck+1}"}))

    circuit = []
    circuit = succ[head[-1]:]
    circuit.insert(0, 0)
    circuit.append(0)
    
    for city in range(len(circuit)-1):
            graphList.append((circuit[city], circuit[city+1], {"kamion": f"k{truck+1}"}))
       
    return graphList

def graph(circuit):
    G = nx.Graph()
    G.add_edges_from(listEdgesColor(circuit))

    # edge color
    color_of_transport={'k1':'blue', 'k2':'orange', 'k3':'pink', 'k4':'green', 'k5':'red', 'k6':'purple', 'k7':'brown', 'k8':'gold', 'k9':'gray',
                        'k10':'cyan', 'k11':'red', 'k12':'blue', 'k13':'orange', 'k14':'pink', 'k15':'green', 'k16':'red', 'k17':'purple', 'k18':'brown', 'k19':'gold', 'k20':'gray',
                        'k21':'cyan', 'k22':'red', 'k23':'blue', 'k24':'orange', 'k25':'pink', 'k26':'green', 'k27':'red', 'k28':'purple', 'k29':'brown', 'k30':'gold', 'k31':'gray',
                        'k32':'cyan', 'k33':'red'}
    transport_colors = [color_of_transport[prop['kamion']] for u, v, prop in G.edges(data=True)]

    # Print graph into window
    plt.figure(figsize=(15,8))
    nx.draw_networkx(G, 
                    node_color="red",
                    edge_color=transport_colors,
                    width=1,
                    node_size=300)
    plt.axis()
    plt.show()

