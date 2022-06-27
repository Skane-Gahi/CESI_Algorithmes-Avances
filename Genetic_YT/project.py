import random, math
import numpy as np

#   PARAMETERS ###############################################
k = 2
v = 4
nbrIndividus = 8
max_iter = 20
nb_colis = 50
random.seed(3)

#   TRAFFIC ##################################################
MATIN = [1.7, 2.2]
MIDI = [0.8, 1.2]
APRES_MIDI = [1.25, 1.7]
NUIT = [0.6, 1]


def matrice_poids(v, periode):
  arr = np.empty((v, v), dtype='int32')
  for i in range(0,v):
    for j in range(0,v):
      if j != i:
        arr[i][j] = round(random.randint(1, 100) * random.uniform(periode[0], periode[1]))
      else:
        arr[i][j] = 0
  
  return arr

matricePoids = matrice_poids(v, MIDI)

# COLIS ######################################################
# AU pif :
VOLUME_COLIS = [1, 3, 5, 8]
CAPACITE_CAMION = 20

def TableauColis(nb_colis):
  tableau = {}
  tableau[0] = random.randint(0, int(nb_colis/2))
  tableau[1] = random.randint(0, int(nb_colis-tableau[0]))
  tableau[2] = random.randint(0, int(nb_colis-(tableau[0]+tableau[1])))
  tableau[3] = nb_colis-(tableau[0]+tableau[1]+tableau[2])
  return tableau

# tableau_colis = TableauColis(nb_colis)
# print(tableau_colis)

def NombreCamion(tableau_colis):
  nb_camion = 1
  capacite = 0
  listeCapacite = []

  for i in range(3, -1, -1):
    for colis in range(tableau_colis[i]):
      if capacite + VOLUME_COLIS[i] < CAPACITE_CAMION:
        capacite += VOLUME_COLIS[i]
      else:
        nb_camion += 1
        listeCapacite.append(capacite)
        capacite = 0 + VOLUME_COLIS[i]

  listeCapacite.append(capacite)
  print(nb_camion)
  print(listeCapacite)

# NombreCamion(tableau_colis)

#   GENERATION ###############################################
#   population : [individu{0,k} [chemins{0,v+1}] ]



def generate_individual(trucksNb, k, matricePoids):
  
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
    for delivery in range(len(truck)-1):
        # set the route in population 
        arr[truck[delivery]][truck[delivery+1]] = 1
    individual.append(arr.copy()*matricePoids.copy())
  return individual
  

def generate_population(matricePoids):
  # Init empty population
  pop = []
  
  for i in range(0,nbrIndividus): # Normalement 8
    # Randomly generate one individual with random genes
    pop.append(generate_individual(k, v, matricePoids))
  return pop


# matricePoids = matrice_poids(v, MIDI)
# a = generate_population(matricePoids)
# print(a)


#   FITNESS ##################################################
def get_sum(element):
  totalSum = 0
  for i in element:
    totalSum += i.sum()
  return totalSum

def sorting(pop):
  pop.sort(key=get_sum, reverse=False)
  return pop

# a = generate_population()
# b = sorting(a)
# print(b)



#   CROSSOVER ################################################
def sub_cross_over(i1, i2):
  
  individual = []
  for i in range(len(i1)):
    if i < (len(i1)/2):
      individual.append(i1[i].copy())
    else:
      individual.append(i2[i].copy())
  return individual

def crossover(pop):
  
  n_pop = []
  for i in range(len(pop)):
    if i == 0:
      n_pop.append(pop[i])
    else:
      n_pop.append(sub_cross_over(pop[0], pop[i]))
  
  return n_pop

# a = generate_population()
# b = sorting(a)
# print(b[0])
# print(b[1])
# c = crossover(b)
# print(c[0])
# print(c[1])




#   MUTATION ##################################################
def mutation(pop, matricePoids):
  # Sauf le 1er individu --> start à 1
  for i in range(1, len(pop)):
    matrice_random = random.randint(0, len(pop[i])-1)

    # gene_to_mutate
    x = math.floor(random.random()*len(pop[0][0]))
    y = math.floor(random.random()*len(pop[0][0]))
 
    if (pop[i][matrice_random][x][y] == 0) :
      pop[i][matrice_random][x][y] = matricePoids[x][y].copy()
    else :
      pop[i][matrice_random][x][y] = 0
  
  return pop

# matricePoids = matrice_poids(v)
# a = generate_population(matricePoids)
# b = sorting(a)
# c = crossover(b)
# d = mutation(c, matricePoids)
# print(d)




#   NEW_POPULATION ############################################
def NewPopulation(n_pop, matricePoids):
  pop = []
  for i in range(len(n_pop)):
    if i < (len(n_pop)/2):
      pop.append(n_pop[i])
    else:
      pop.append(generate_individual(k, v, matricePoids))

  return pop


# Loop ########################################################
def Loop(pop):
  if pop != []:
    a = pop
  else:
    a = generate_population(matricePoids)
  b = sorting(a)
  # print(b[0])
  # print("Classement : ")
  # print(b)
  c = crossover(b)
  # print("Crossover : ")
  # print(c)
  d = mutation(c, matricePoids)
  # print(c[0])
  # print("Mutation : ")
  # print(d)
  e = NewPopulation(d, matricePoids)
  # print("Final : ")
  # print(e)
  return e