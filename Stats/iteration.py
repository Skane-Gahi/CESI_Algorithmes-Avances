import numpy as np
import random
import matplotlib.pyplot as plt

#   PARAMETERS ###############################################
V = 100
INDIVIDUAL = 8

NB_COLIS = 50


#   TRAFFIC ##################################################
MATIN = [1.7, 2.2]
MIDI = [0.8, 1.2]
APRES_MIDI = [1.25, 1.7]
NUIT = [0.6, 1]

# CALCUL DU NOMBRE DE CAMIONS ################################
VOLUME_COLIS = [1, 3, 5, 8]
CAPACITE_CAMION = 50

def TableauColis(nb_colis):
  tableau = {}
  tableau[0] = random.randint(0, int(nb_colis/2))
  tableau[1] = random.randint(0, int(nb_colis-tableau[0]))
  tableau[2] = random.randint(0, int(nb_colis-(tableau[0]+tableau[1])))
  tableau[3] = nb_colis-(tableau[0]+tableau[1]+tableau[2])
  return tableau

def sub_nombreCamion(tab_colis, i, capacite):
    for _ in range(tab_colis[i]):
        if capacite + VOLUME_COLIS[i] < CAPACITE_CAMION and tab_colis[i] > 0:
            capacite += VOLUME_COLIS[i]
            tab_colis[i] -= 1
        elif i > 0:
            for j in range(i-1, -1, -1):
                for _ in range(tab_colis[j]):
                    if capacite + VOLUME_COLIS[j] < CAPACITE_CAMION and tab_colis[j] > 0:
                        capacite += VOLUME_COLIS[j]
                        tab_colis[j] -= 1

    for j in range(i-1, -1, -1):
                for _ in range(tab_colis[j]):
                    if capacite + VOLUME_COLIS[j] < CAPACITE_CAMION and tab_colis[j] > 0:
                        capacite += VOLUME_COLIS[j]
                        tab_colis[j] -= 1

    return capacite

def NombreCamion(tableau_colis):
    tab_colis = tableau_colis.copy()
    nb_camion = 1
    capacite = 0
    listeCapacite = []
    
    while any(x != 0 for x in tab_colis.values()):

        i = 3
        capacite = sub_nombreCamion(tab_colis, i, capacite)
        
        listeCapacite.append(capacite)
        capacite = 0
        nb_camion += 1
        i = 3
                
    listeCapacite.append(capacite)
    # print(tab_colis)
    # print(listeCapacite)
    return nb_camion

tableau_colis = TableauColis(NB_COLIS)
k = NombreCamion(tableau_colis)
# print('Nombre camion : ', k)

#   MATRICE DES POIDS ########################################
def matrice_poids(v, periode):
  arr = np.empty((v, v), dtype='int32')
  for i in range(0,v):
    for j in range(0,v):
      if j != i:
        arr[i][j] = round(random.randint(1, 100) * random.uniform(periode[0], periode[1]))
      else:
        arr[i][j] = 0
  
  return arr

MATRICE_POIDS = matrice_poids(V, MIDI)

# Generation #################################################
def Population():
    pop = []
    for _ in range(0, INDIVIDUAL):
        # randomList = [0]
        randomList = random.sample(range(1, V), V-1)
        # randomList.extend([0])
        truckIdx = random.sample(range(1, V-1), k-1)
        pop.append([randomList, truckIdx])
        
    return pop

#   Only for new gen ########################################
def individu():
    
    # randomList = [0]
    randomList = random.sample(range(1, V), V-1)
    # randomList.extend([0])
    truckIdx = random.sample(range(1, V-1), k-1)

    return [randomList, truckIdx]

#   Fitness #################################################
def get_sum(path):
    totalSum = 0
    element0 = path[0].copy()
    element1 = path[1].copy()
    
    #   Ajout du depot à l'interieur (fin du 1 camion, debut du 2ème, ...)
    for index in element1:
        for i in range(0,2):
            element0.insert(index, 0)

    #   Ajout du depot au debut et à la fin
    element0.append(0)
    element0.insert(0, 0)

    for i in range(len(element0)-1):
        totalSum += MATRICE_POIDS[element0[i]][element0[i+1]]
   
    return totalSum

def Fitness(pop):
    pop.sort(key=get_sum, reverse=False)
    return pop


#   Crossover ###############################################
def sub_crossover(i1, i2):
    rdmStartIdx = random.randint(0, len(i1[0])-2)
    rdmLength = random.randint(2, (len(i1[0]))-rdmStartIdx)
    idxList = list(range(rdmStartIdx, rdmStartIdx+rdmLength))
    child = [0] * (len(i1[0]))

    for i in idxList:
        child[i] = i1[0][i]
    for i in range(0, len(i2[0])):
        if child[i] == 0:
            if i2[0][i] not in child:
                child[i] = i2[0][i]
            else:
                for j in idxList:     
                    if i2[0][j] not in child:
                        child[i] = i2[0][j]
          
    rdmTruckIdx = random.randint(0, 1)
    truckIdx = i1[1] if rdmTruckIdx == 0 else i2[1]
    return [child, truckIdx]

def Crossover(pop):
    n_pop = []
    for i in range(len(pop)):
       
        if i == 0:
            n_pop.append(pop[i])
        else:
            n_pop.append(sub_crossover(pop[0], pop[i]))
       
    return n_pop


#   Mutation ################################################
def Mutation(pop):
    n = 0
    for i in pop:
        if n > 0:
            rdmIdx1 = random.randint(0, len(i[0])-1)
            rdmIdx2 = random.randint(0, len(i[0])-1)
            tmp = i[0][rdmIdx1]
            i[0][rdmIdx1] = i[0][rdmIdx2]
            i[0][rdmIdx2] = tmp
        n += 1

    return pop

#   NEW_POPULATION ############################################
def NewPopulation(pop):
    pop = Fitness(pop)
    n_pop = []
    for i in range(len(pop)):
        if i < (len(pop)/2):
            n_pop.append(pop[i])
        else:
            n_pop.append(individu())

    return n_pop


# Loop ########################################################
def Loop(pop):
    if pop == []:
        pop = Population()
    
    pop = Fitness(pop)
    pop = Crossover(pop)
    pop = Mutation(pop)
    pop = NewPopulation(pop)
        
    return pop


#   MAIN ######################################################

def Main(max_iter):
    population = []
    iter = 0
    bestScore = 9999999
    while iter < max_iter :

        if population != []:
            
            for individual in population:
                tmpBestScore = get_sum(individual)
             
                if tmpBestScore < bestScore:
                    bestScore = tmpBestScore
  
        population = Loop(population)
        iter += 1

    if population != []:
     
        for individual in population:
            tmpBestScore = get_sum(individual) 
           
            if tmpBestScore < bestScore:
                bestScore = tmpBestScore

        print("Iteration : ", str(iter), " - Best Score : ", str(bestScore))
        return [iter, bestScore]

# STAT #########################################################

def Stat():
    startIter = 10
    endIter = 101
    p = 10
    #   X
    iterNbr = []
    #   Y
    fitness = []
    for i in range(startIter, endIter, p):
        max_iter = i
        result = Main(max_iter)
        iterNbr.append(result[0])
        fitness.append(result[1])
    
    plt.plot(iterNbr, fitness, label="Fitness en fonction du nomre d'itération")
    plt.legend()
    plt.show()


Stat()
# Reste à print le chart
# Changer le liste.py avec la selection après la mutation et avant la regeneration aléatoire (fitness dans le new gen)