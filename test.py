import random
import numpy as np
import numpy.random as rnd

# algorithm parameters

# number of cities
n = 10 
# number of nodes      
v = n+1     
# number of individual in each generation    
popSize = 4   

# number of genetic iterations
generations = 100
# number of packages to be delivered 
packages = 10   

# list of packages 
l = [1, 3, 5, 8] 
# trucks capactity
truckCapacity = 20

# traffic's coefficients 
traffic = [1.7, 2.2]
A = rnd.randint(low=1, high=100, size=(v,v)) * rnd.uniform(traffic[0], traffic[1])

def PackagesDistri(packages:int) -> dict:
    """Distribution of packages between volumes categories"""
    # create dictionnary to be returned
    L = {}
    # fill dictionnary
    L[0] = rnd.randint(0, int(packages/2))
    L[1] = rnd.randint(0, int(packages-L[0]))
    L[2] = rnd.randint(0, int(packages-(L[0]+L[1])))
    L[3] = packages-(L[0]+L[1]+L[2])
    # then return it
    return L

def CalcTruckNb(pkgDistri:dict) -> int:
    """Calculate the optimal number of trucks depending on pkgDistri"""
    truckNb = 1
    occupied = 0
    
    while any(x != 0 for x in pkgDistri.values()):

        i = 3
        occupied = 0

        for _ in range(pkgDistri[i]):
            if occupied + l[i] < truckCapacity and pkgDistri[i] > 0:
                occupied += l[i]
                pkgDistri[i] -= 1
            elif i > 0:
                for j in range(i-1, -1, -1):
                    for _ in range(pkgDistri[j]):
                        if occupied + l[j] < truckCapacity and pkgDistri[j] > 0:
                            occupied += l[j]
                            pkgDistri[j] -= 1

        for j in range(i-1, -1, -1):
            for _ in range(pkgDistri[j]):
                if occupied + l[j] < truckCapacity and pkgDistri[j] > 0:
                    occupied += l[j]
                    pkgDistri[j] -= 1

        truckNb += 1 
    return truckNb

L = PackagesDistri(packages)
k = CalcTruckNb(L)
print(f"Number of trucks needed : {k}")

def Population() -> list:
    # create empty population
    pop = []
    # iterate over individuals
    for _ in range(0, popSize):
        # generate random successors
        rndSucc = random.sample(range(1, v), v-1)
        # generate random header (corresponding to trucks)
        rndHead = random.sample(range(1, v-1), k-1)
        # add result to population
        pop.append([rndSucc, rndHead])
    # return population
    return pop

def CalcFitness(individual:list) -> any:
    """Calculate the fitness of a given individual"""
    fitness = 0
    # copy individual to avoid conflicts
    succ = individual[0].copy()
    head = individual[1].copy()
    
    # add arrival/departure to depository between trucks
    for index in head:
        for i in range(0,2):
            succ.insert(index, 0)

    # add departure of first truck and arrival of last one
    succ.append(0)
    succ.insert(0, 0)
    # iterate over successors
    for i in range(len(succ)-1):
        fitness += A[succ[i]][succ[i+1]]
    # return fitness value
    return fitness

def SortFitness(pop:list) -> list:
    """Sort fitness in given population from best to worst"""
    pop.sort(key=CalcFitness, reverse=False)
    return pop

def Crossover(pop:list) -> list:
    """Partially mapped crossover between best fitness and the rest of a given population"""
    # assign best fitness to parent 1
    parent1 = pop[0]
    # add it to new population
    newPop = [parent1]
    # iterate over second parents in population
    for i in range(1, len(pop)):
        # assign second parent
        parent2 = pop[i]
        # randomly select the portion to cross
        rndStartIdx = rnd.randint(0, len(parent1[0])-2)
        rdnLength = rnd.randint(2, (len(parent1[0]))-rndStartIdx)
        # mapping list
        idxList = list(range(rndStartIdx, rndStartIdx+rdnLength))

        # create successors list with values of parent1
        succ = [parent1[0][i] if i in idxList else 0 for i in range(len(parent1[0]))]
        # then fill the rest with parent2 values
        for i in range(0, len(parent2[0])):
            if succ[i] == 0:
                if parent2[0][i] not in succ:
                    succ[i] = parent2[0][i]
                # else if value is already in successors
                else:
                    # try each value of parent2 that were overwritten
                    for j in idxList:     
                        if parent2[0][j] not in succ:
                            succ[i] = parent2[0][j]

        # randomly select between parent1's head and parent2's head
        rndTruckIdx = rnd.randint(0, 1)
        head = parent1[1] if rndTruckIdx == 0 else parent2[1]
        newPop.append([succ, head])
    # return new population
    return newPop

def Mutation(pop:list) -> list:
    """Mutation process on given population (switch two randomly chosen successors)"""
    # iterate over individuals in population
    for individual in pop[1:]:
        # randomly select two indexes to be switched
        rndIdx1 = rnd.randint(0, len(individual[0])-1)
        rndIdx2 = rnd.randint(0, len(individual[0])-1)

        # switch values placed at those indexes
        tmp = individual[0][rndIdx1]
        individual[0][rndIdx1] = individual[0][rndIdx2]
        individual[0][rndIdx2] = tmp
    # return resulted population
    return pop

# assign initial population
pop = Population()
# set the counter of iterations
iter = 0

bestScore = 999999

# while iter < generations:
#     pop = SortFitness(pop)
#     pop = Crossover(pop)
#     pop = Mutation(pop)

    

#     iter+=1

def individu():
    
    # randomList = [0]
    randomList = random.sample(range(1, v), v-1)
    # randomList.extend([0])
    truckIdx = random.sample(range(1, v-1), k-1)

    return [randomList, truckIdx]

def NewPopulation(pop):
    n_pop = []
    for i in range(len(pop)):
        if i < (len(pop)/2):
            n_pop.append(pop[i])
        else:
            n_pop.append(individu())

    return n_pop

def Loop(pop):
    if pop == []:
        pop = Population()
    
    pop = SortFitness(pop)
    pop = Crossover(pop)
    pop = Mutation(pop)
    pop = NewPopulation(pop)
        
    return pop

while iter < generations :
    print('ITERATION : ', str(iter))
    print(pop)
    if pop != []:
        tmpList = []
        for individual in pop:
            tmpBestScore = CalcFitness(individual)
            tmpList.append(tmpBestScore)
            if tmpBestScore < bestScore:
                bestScore = tmpBestScore
        print(tmpList)
        print("Best Score : ", str(bestScore), '\n')

    pop = Loop(pop)
    iter += 1