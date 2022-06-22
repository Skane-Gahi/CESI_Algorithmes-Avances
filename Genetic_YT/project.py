import random, math, numpy

#   PARAMETERS ###############################################
k = 5
v = 10

#   GENERATION ###############################################
#   population : [individu{0,k} [chemins{0,v+1}] ]
#   Faire une matrice v*v plutot, une matrice des poids des aretes

def liste_camion(v):
    subPath = []
    arr = numpy.empty((v, v), dtype='int32')
    for i in range(0,v):
        for j in range(0,v):
            arr[i][j] = random.randint(0, 1)
        subPath.append(arr) 
    
    return subPath

def generate_individual(k, v):
  path = []
  for i in range(0,k):
    path.append(liste_camion(v))
  
  return path

def generate_population():
  # Init empty population
  pop = []
  
  for i in range(0,2):
    # Randomly generate one individual with random genes
    pop.append(generate_individual(k, v))
  
  return pop

# print(generate_population())
print(liste_camion(2))