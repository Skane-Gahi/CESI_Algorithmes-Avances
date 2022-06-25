import random, math, numpy

#   PARAMETERS ###############################################
k = 5
v = 5
nbrIndividus = 10
max_iter = 100
nb_colis = 50
random.seed(3)

#   TRAFFIC ##################################################
MATIN = [1.7, 2.2]
MIDI = [0.8, 1.2]
APRES_MIDI = [1.25, 1.7]
NUIT = [0.6, 1]


def matrice_poids(v, periode):
  arr = numpy.empty((v, v), dtype='int32')
  for i in range(0,v):
    for j in range(0,v):
      arr[i][j] = round(random.randint(1, 100) * random.uniform(periode[0], periode[1]))
  
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

tableau_colis = TableauColis(nb_colis)
print(tableau_colis)

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

NombreCamion(tableau_colis)

#   GENERATION ###############################################
#   population : [individu{0,k} [chemins{0,v+1}] ]



def matrice_camion(v):
  
  arr = numpy.empty((v, v), dtype='int32')
  for i in range(0,v):
    for j in range(0,v):
      if i != j:
        arr[i][j] = random.randint(0, 1) 
      else:
        arr[i][j] = 0 # Contrainte de pas boucler sur la même ville (diagonales à 0)
  
  # Contrainte de partir et revenir au depot {0,0}
  indexLigne = random.randint(1, v)
  indexColonne = random.randint(1, v) 
  arr[indexLigne][0] = 1
  if indexColonne != indexLigne:
    arr[0][indexColonne] = 1
  else:
    try:
      arr[0][indexColonne+1] = 1
    except:
      arr[0][indexColonne-1] = 1
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