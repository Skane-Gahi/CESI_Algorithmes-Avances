import numpy as np

# Inputs data of our problem
n = 10 # number of cities
v = n+1 # number of nodes
k = 2 # number of trucks

N, K = [i for i in range(1, n+1)], [i for i in range(1, k+1)] # sets of cities and trucks
# set of nodes (cities + warehouse)
V = [0] + N 
# set of weighted arcs 
A = np.random.randint(low=0, high=5+1, size=(v,v)) 

# trucks capacity
C = pow(5,3) 

def generatePopu(indivNb:int, trucksNb:int, nodesNb:int) -> np.ndarray:
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

# Creating the initial population
popuSize = 6
popu = generatePopu(popuSize, k, v)
numParents = np.uint8(popuSize/2)

def getFitness(popu:list, arcs:np.ndarray) -> int:
    """ 
    Calculating the fitness value of each solution in the current population.\n
    The fitness function caulcuates the sum of products between each input and its corresponding weight.
    """
    # create fitness list
    allFitness = []
    # iterating over individual in population
    for genome in range(popu.shape[0]):
        # set the fitness to 0
        fitness = 0
        # iterating over genes in each individual
        for gene in range(popu[genome].shape[0]):
            # incrementing fitness by summing the multiplication of the gene by distances matrix
            fitness += (np.sum(popu[genome, gene, :]*arcs))
        # append result to list of fitness
        allFitness.append(fitness)
    return allFitness

def naturalSelect(popu:np.ndarray, fitness:list, num_parents:int) -> np.ndarray:
    """
    Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    """
    # creating empty matric to store parents
    parents = np.empty((num_parents, popu.shape[1], popu.shape[2], popu.shape[3]), dtype=np.uint0)
    # iterating over rows in parents matrix
    for parentIdx in range(num_parents):
        # get the index of smallest fitness value
        minFitnessIdx = fitness.index(min([i for i in fitness if i > 0]))
        # set the parent equal to the actual best individual
        parents[parentIdx, :] = popu[minFitnessIdx, :]
        # set current min fitness to -1 in order to ignore it next time
        fitness[minFitnessIdx] = -1
    return parents

def crossover(parents:np.ndarray, offspringSize:tuple) -> np.ndarray:
    """
    Crossover between a set of given parents and return resulted children
    """
    offspring = np.empty(offspringSize, dtype=np.uint0)
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossoverPoint = np.uint8(offspringSize[1]/2)

    for k in range(offspringSize[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossoverPoint] = parents[parent1_idx, 0:crossoverPoint].copy()
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossoverPoint:] = parents[parent2_idx, crossoverPoint:].copy()
    return offspring

def checkCity(popu:np.ndarray) -> list:
    """
    Check any individual of a given population if any city has not been delivered
    """
    # list to store not delivered city numbers
    notDelivered = [ [] for _ in range(popu.shape[0])]

    # iterating over individuals in population
    for idx, individual in enumerate(popu):
        # iterating over lines (corresponding to cities)
        for city in range(individual[0].shape[0]):
            # set a counter to 0
            counter = 0
            # iterating over trucks
            for truck in range(individual.shape[0]):
                # count occurences of 1 in truck circuit for current city
                counter += np.count_nonzero(individual[truck, city, :] == 1)
            # if no trucks has delivered current city
            if counter < 1:
                # add it to the list for current individual
                notDelivered[idx].append(city)
    # return not delivered cities
    return notDelivered

def mutation(offsprings:np.ndarray) -> np.ndarray:
    """
    Mutation of given offsprings
    """
    print(checkCity(offsprings))
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offsprings.shape[0]):
        # The random value to be added to the gene.
        n = offsprings[0][0].shape[0]
        randomGene = np.random.randint(0, 2, (n,n))
        randomTruck = np.random.randint(0, offsprings.shape[0]-1)
        offsprings[idx, randomTruck] =  randomGene
    return offsprings

# number of generations aka. number of iterations
numGenerations = 10
for generation in range(1, numGenerations+1):
    # Measing the fitness of each chromosome in the population.
    fitness = getFitness(popu, A)

    # Selecting the best parents in the population for mating.
    parents = naturalSelect(popu, fitness, numParents)

    # Generating next generation using crossover.
    offsprings = crossover(parents, offspringSize=(popuSize - parents.shape[0], k, v, v))

    # Adding some variations to the offsrping using mutation.
    mutated_offsprings = mutation(offsprings)

    # Creating the new population based on the parents and offspring.
    popu[0:parents.shape[0], :] = parents
    popu[parents.shape[0]:, :] = mutated_offsprings

    # The best result in the current iteration.
    currentFitness = getFitness(popu=popu, arcs=A)
    print("All fitnesses : ", currentFitness)
    print("Best result : ", min(currentFitness))

# print(popu[currentFitness.index(min(currentFitness)), :])

# print(generatePopu(popuSize, k, v))