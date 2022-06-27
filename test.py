import numpy as np

def generatePopu(indivNb:int, trucksNb:int, nodesNb:int) -> any:
    """
    Generate initial population with constraints respected
    """
    # generate an initial population full of zero
    popu = np.zeros((indivNb, trucksNb, nodesNb, nodesNb), dtype=np.uint0)

    # list to store trucks circuits
    circuits = [ [] for _ in range(trucksNb)]
    # iterating for each individual to generate
    for individual in range(indivNb):
        # iterate over cities to be delivered
        for city in range(1, nodesNb):
            # choose a random truck to deliver
            rndTruck = np.random.randint(low=0, high=trucksNb, size=1)[0]
            circuits[rndTruck].append(city)
        # iterate over trucks circuits
        for idx, truck in enumerate(circuits):
            # if the truck has been given at least one city
            if len(truck) > 0:
                # had departure and arrival to depository
                truck.append(0)
                truck.insert(0, 0)
            # iterating over deliveries of trucks
            for delivery in range(len(truck)-1):
                # set the route in population 
                popu[individual, idx, truck[delivery], truck[delivery+1]] = 1
        # reset circuits for next individual generation
        circuits = [ [] for _ in range(trucksNb)]
    return popu

# print(generatePopu(3, 2, 4))

def matrice_camion(v, trucksNb):
  
    # list to store trucks circuits
    circuits = [ [] for _ in range(trucksNb)]
    individual = []

    for city in range(1, v):
        # choose a random truck to deliver
        rndTruck = np.random.randint(low=0, high=trucksNb, size=1)[0]
        circuits[rndTruck].append(city)
    
    # iterate over trucks circuits
    for truck in circuits:
        arr = np.zeros((v, v), dtype='int32')
        # if the truck has been given at least one city
        if len(truck) > 0:
            # had departure and arrival to depository
            truck.append(0)
            truck.insert(0, 0)
        # iterating over deliveries of trucks
        print(truck)
        for delivery in range(len(truck)-1):
            # set the route in population 
            arr[truck[delivery]][truck[delivery+1]] = 1
        individual.append(arr.copy())
    return individual

print(matrice_camion(4, 2))