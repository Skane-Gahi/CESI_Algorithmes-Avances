from liste import *

#   MAIN #############################################################
population = []
iter = 0
bestScore = 9999999


while iter < MAX_ITER :
    print('ITERATION : ', str(iter))

    if population != []:
        tmpList = []
        for individual in population:
            tmpBestScore = get_sum(individual)
            tmpList.append(tmpBestScore)
            if tmpBestScore < bestScore:
                bestScore = tmpBestScore
        print(tmpList)
        print("Best Score : ", str(bestScore), '\n')

    # print(population)   
    population = Loop(population)
    iter += 1

if population != []:
    print('ITERATION : ', str(iter))
    tmpList = []
    for individual in population:
        tmpBestScore = get_sum(individual) 
        tmpList.append(tmpBestScore)
        if tmpBestScore < bestScore:
            bestScore = tmpBestScore
    print(tmpList)
    print("Best Score : ", str(bestScore))
    # print(population)
            