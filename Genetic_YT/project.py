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

