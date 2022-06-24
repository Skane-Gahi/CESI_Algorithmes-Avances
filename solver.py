import numpy as np

# Inputs data of our problem
n = 100 # number of cities
k = 5 # number of trucks

N, K = [i for i in range(1, n+1)], [i for i in range(1, k+1)] # sets of cities and trucks
# set of nodes (cities + warehouse)
V = [0] + N 
# set of weighted arcs 
A = np.random.randint(low=0, high=1000+1, size=(n,n)) 

# trucks capacity
C = pow(5,3) 

# Creating the initial population
popuSize = 6
popu = np.random.randint(low=0, high=1+1, size=(popuSize,k,n,n))
numParents:int = np.uint8(popuSize/2)

print(A)

def getFitness(popu:list, arcs:np.ndarray) -> int:
    """ 
    Calculating the fitness value of each solution in the current population.\n
    The fitness function caulcuates the sum of products between each input and its corresponding weight.
    """
    allFitness = list()
    for genome in popu:
        fitness = 0
        for gene in genome:
            fitness += (np.sum(gene*arcs))
        allFitness.append(fitness)
    return allFitness

def naturalSelect(popu:np.ndarray, fitness:list, num_parents:int) -> any:
    """
    Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    """
    parents = np.empty((num_parents, popu.shape[1], popu.shape[2], popu.shape[3]), dtype=np.uint0)
    for parent_idx in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_idx, :] = popu[max_fitness_idx, :]
        fitness[max_fitness_idx] = -1

    return parents

def crossover(parents:np.ndarray, offspringSize) -> any:
    offspring = np.empty(offspringSize, dtype=np.uint0)
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossoverPoint = np.uint8(offspringSize[1]/2)

    for k in range(offspringSize[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossoverPoint] = parents[parent1_idx, 0:crossoverPoint]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossoverPoint:] = parents[parent2_idx, crossoverPoint:]
    return offspring

def mutation(offsprings) -> any:
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offsprings.shape[0]):
        # The random value to be added to the gene.
        n = offsprings[0][0].shape[0]
        randomGene = np.random.randint(0, 2, (n,n))
        randomTruck = np.random.randint(0, offsprings.shape[0]-1)
        offsprings[idx, randomTruck] =  randomGene
    return offsprings

# number of generations aka. number of iterations
num_generations = 100
for generation in range(num_generations):
    print("Generation : ", generation)
    # Measing the fitness of each chromosome in the population.
    fitness = getFitness(popu, A)

    # Selecting the best parents in the population for mating.
    parents = naturalSelect(popu, fitness, numParents)
    # print(parents.tolist())

    # Generating next generation using crossover.
    offsprings = crossover(parents, offspringSize=(popuSize - parents.shape[0], k, n, n))
    # print(offsprings.tolist())

    # Adding some variations to the offsrping using mutation.
    mutated_offsprings = mutation(offsprings)

    # Creating the new population based on the parents and offspring.
    popu[0:parents.shape[0], :] = parents
    popu[parents.shape[0]:, :] = mutated_offsprings

    # The best result in the current iteration.
    print("Best result : ", np.max(np.sum(popu*A, axis=1)))