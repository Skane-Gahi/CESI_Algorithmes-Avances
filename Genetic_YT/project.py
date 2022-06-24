import random, math, numpy

#   PARAMETERS ###############################################
k = 5
v = 30
nbrIndividus = 10
max_iter = 100

def matrice_poids(v):
    arr = numpy.empty((v, v), dtype='int32')
    for i in range(0,v):
      for j in range(0,v):
        arr[i][j] = random.randint(1, 100) 
    
    return arr

matricePoids = matrice_poids(v)

#   GENERATION ###############################################
#   population : [individu{0,k} [chemins{0,v+1}] ]



def matrice_camion(v):
  
  arr = numpy.empty((v, v), dtype='int32')
  for i in range(0,v):
    for j in range(0,v):
      arr[i][j] = random.randint(0, 1) 
  
  # Contrainte de partir et revenir au depot (ici en {0,0})
  arr[0][0] = 1
  return arr.copy()

def generate_individual(k, v, matricePoids):
  path = []
  for i in range(0,k):
    path.append(matrice_camion(v)*matricePoids.copy())
  
  cases_manquantes = []
  for i in range(0,v):
    for j in range(0,v): 
      for m in path:
        if m[i][j] == 0:
          cases_manquantes.append([i, j])
        else:
          try:
            cases_manquantes.remove([i, j])
          except:
            z=0

  for case in cases_manquantes:
    kRandom = random.randint(0, k-1)
    path[kRandom][case[0]][case[1]] = matricePoids[case[0]][case[1]].copy()
  return path

def generate_population(matricePoids):
  # Init empty population
  pop = []
  
  for i in range(0,nbrIndividus): # Normalement 8
    # Randomly generate one individual with random genes
    pop.append(generate_individual(k, v, matricePoids))
  return pop

# print(matrice_camion(2))
# matricePoids = matrice_poids(v)
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