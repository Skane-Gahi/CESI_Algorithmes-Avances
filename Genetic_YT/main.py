from project import *

#   YT #############################################################
# population = []
# max_iter = 10
# iter = 0

def MainLoopYT(population):
    if population == []:
        pop = generate_population()
        print("START : ", pop)
    else:
        pop = population

    sortedPop = sorting(pop)
    # print(sortedPop)

    crossoveredPop = crossover(sortedPop)
    # print(crossoveredPop)

    mutationnedPop = mutation(crossoveredPop)
    # print(mutationnedPop)

    finalPop = NewPopulation(mutationnedPop)
    # print(finalPop)
    return finalPop

# while iter < max_iter :

#     if population != []:
#         if get_sum(population[0]) == 8:
#             print(population)
#             break
        
#     population = MainLoopYT(population)
#     print('ITERATION : ', str(iter))
#     iter += 1

#####################   MAIN    #######################################


a = generate_population(matricePoids)
print("Géneration de base : ")
print(a)
b = sorting(a)
print("Classement : ")
print(b)
c = crossover(b)
print("Crossover : ")
print(c)
d = mutation(c, matricePoids)
print("Mutation : ")
print(d)
e = NewPopulation(d, matricePoids)
print("Final : ")
print(e)