import random, math

#   GENERATION ###############################################
def generate_individual():
  individual = []
  for i in range(0,8):
    individual.append(random.randint(0, 1))
  
  return individual

def generate_population():
  # Init empty population
  pop = []
  for i in range(0,8):
    # Randomly generate one individual with random genes
    pop.append(generate_individual())
  
  return pop

#   FITNESS ##################################################
def get_sum(element):
    return sum(element)

def sorting(pop):
    pop.sort(key=get_sum, reverse=True)
    return pop

#   CROSSOVER ################################################
def sub_cross_over(i1, i2):
  individual = [
    i1[0],
    i1[1],
    i1[2],
    i1[3],
    i2[4],
    i2[5],
    i2[6],
    i2[7]
  ]
  return individual

def crossover(pop):
  n_pop = []
  n_pop.append(pop[0])
  n_pop.append(sub_cross_over(pop[0], pop[1]))
  n_pop.append(sub_cross_over(pop[0], pop[2]))
  n_pop.append(sub_cross_over(pop[1], pop[2]))

  return n_pop

#   MUTATION ##################################################
def mutation(pop):
  for i in pop:
      
      gene_to_mutate = math.floor(random.random()*len(i))
      if (i[gene_to_mutate] == 0) :
          i[gene_to_mutate] = 1
      else :
          i[gene_to_mutate] = 0

  return pop
 
#   NEW_POPULATION ############################################
def NewPopulation(n_pop):
    pop = []
    pop.append(n_pop[0])
    pop.append(n_pop[1])
    pop.append(n_pop[2])
    pop.append(n_pop[3])

    pop.append(generate_individual())
    pop.append(generate_individual())
    pop.append(generate_individual())
    pop.append(generate_individual())

    return pop

