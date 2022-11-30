from map import Map
from GA.GA import GA
from DE.DE import DE
from PSO.PSO import PSO
from ACO.ACO import ACO
import cv2
import numpy as np
import time


def get_best(best_fitness, fitness, gen_x, gen_y, best_path_x, best_path_y):
    best_index = np.argmax(fitness)
    if fitness[best_index] > best_fitness:
        best_fitness = fitness[best_index]
        best_path_x = gen_x[best_index, :]
        best_path_y = gen_y[best_index, :]
    return best_fitness, best_path_x, best_path_y


def GASolve():
    map = Map()
    map.draw_map()
    time_start = time.time()
    ga = GA(map.obstacle)
    gen_x, gen_y = ga.init_generation()
    collisions = ga.lineCollision(gen_x, gen_y) 
    
    fitness = ga.calFitness(gen_x, gen_y, collisions)
    best_fitness = 0.0
    best_path_x = None
    best_path_y = None
    best_fitness, best_path_x, best_path_y = get_best(best_fitness, fitness, gen_x, gen_y, best_path_x, best_path_y)
    for i in range(ga.generation_number):
        gen_x, gen_y = ga.select(gen_x, gen_y, fitness)
        gen_x, gen_y = ga.cross_over(gen_x, gen_y, fitness)
        gen_x, gen_y = ga.mutate(gen_x, gen_y, fitness)
        collisions = ga.lineCollision(gen_x, gen_y)
        fitness = ga.calFitness(gen_x, gen_y, collisions)   
        best_fitness, best_path_x, best_path_y = get_best(best_fitness, fitness, gen_x, gen_y, best_path_x, best_path_y)
    print("fitness:", best_fitness)
    dis = 0
    last_x, last_y = 50, 100
    for path_x, path_y in zip(best_path_x, best_path_y):
        dis += np.sqrt((path_x - last_x) ** 2 + (path_y - last_y) ** 2)
        last_x = path_x
        last_y = path_y
        print("=>", (int(path_x), int(path_y)))
    print("distance:", dis)
    time_end = time.time()
    print("time cost:", time_end - time_start, "s")
    map.draw_path(best_path_x, best_path_y)
    cv2.imshow("map", map.image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def DESolve():
    map = Map()
    map.draw_map()
    time_start = time.time()
    de = DE(map.obstacle)
    gen_x, gen_y = de.init_generation()
    collisions = de.lineCollision(gen_x, gen_y) 
    
    fitness = de.CalculateFitness(gen_x, gen_y, collisions)
    best_fitness = 0.0
    best_path_x = None
    best_path_y = None
    best_fitness, best_path_x, best_path_y = get_best(best_fitness, fitness, gen_x, gen_y, best_path_x, best_path_y)
    for i in range(de.generation_number):
        gen_mutation_x, gen_mutation_y = de.mutate(gen_x, gen_y)
        gen_crossover_x, gen_crossover_y = de.cross_over(gen_x, gen_y, gen_mutation_x, gen_mutation_y)
        gen_x, gen_y = de.select(gen_x, gen_y, gen_crossover_x, gen_crossover_y)
        collisions = de.lineCollision(gen_x, gen_y)
        fitness = de.CalculateFitness(gen_x, gen_y, collisions)   
        best_fitness, best_path_x, best_path_y = get_best(best_fitness, fitness, gen_x, gen_y, best_path_x, best_path_y)
    print("fitness:", best_fitness)
    dis = 0
    last_x, last_y = 50, 100
    for path_x, path_y in zip(best_path_x, best_path_y):
        dis += np.sqrt((path_x - last_x) ** 2 + (path_y - last_y) ** 2)
        last_x = path_x
        last_y = path_y
        print("=>", (int(path_x), int(path_y)))
    print("distance:", dis)
    time_end = time.time()
    print("time cost:", time_end - time_start, "s")
    map.draw_path(best_path_x, best_path_y)
    cv2.imshow("map", map.image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def PSOSolve():
    map = Map()
    map.draw_map()
    time_start = time.time()
    pso = PSO(map.obstacle)
    gen_x, gen_y = pso.init_generation()
    vx, vy = pso.init_velocity() 
    
    pbest = np.zeros(pso.population_size)
    pidx = np.zeros((pso.population_size, pso.dim + 2))
    pidy = np.zeros((pso.population_size, pso.dim + 2))

    max_best = 0
    maxpgdx = np.zeros(pso.dim + 2)
    maxpgdy = np.zeros(pso.dim + 2)
    max_fitvalue = []
    

    for i in range(pso.generation_number):
        collisions = pso.lineCollision(gen_x, gen_y)
        fitness = pso.calFitness(gen_x, gen_y, collisions)   
        pbest, pidx, pidy, gbest, pgdx, pgdy = pso.fit_cmp(gen_x, gen_y, fitness, pbest, pidx, pidy)
        vx, vy = pso.update_velocity(vx, vy, gen_x, gen_y, pidx, pidy, pgdx, pgdy)
        gen_x, gen_y = pso.update_pos(gen_x, gen_y, vx, vy)
        if max_best < gbest:
            max_best = gbest
            maxpgdx = pgdx
            maxpgdy = pgdy
        max_fitvalue.append(max_best)
        pso.w = pso.w - (pso.w - 0.3) / pso.generation_number

    print("fitness:", max_best)
    dis = 0
    last_x, last_y = 50, 100
    for path_x, path_y in zip(maxpgdx, maxpgdy):
        dis += np.sqrt((path_x - last_x) ** 2 + (path_y - last_y) ** 2)
        last_x = path_x
        last_y = path_y
        print("=>", (int(path_x), int(path_y)))
    print("distance:", dis)
    time_end = time.time()
    print("time cost:", time_end - time_start, "s")
    map.draw_path(maxpgdx, maxpgdy)
    cv2.imshow("map", map.image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ACOSolve():
    map = Map()
    map.draw_map()
    time_start = time.time()
    aco = ACO(map.obstacle)
    aco.set_obstacle()


    # For Debugging
    # for i in range(aco.enx + 1):
    #     for j in range(aco.eny + 1):
    #         if aco.obs[i, j]:
    #             cv2.circle(map.image, (int(i * aco.precision), int(j * aco.precision)),5,(0,255,0),thickness=2) 
    #         else:
    #             cv2.circle(map.image, (int(i * aco.precision), int(j * aco.precision)),5,(2550, 0,0),thickness=2) 
    # cv2.imshow("map", map.image)
    # cv2.waitKey(0)

    # input()


    it = 0
    while True:
        if it >= aco.NC:
            break
        it += 1
        px, py, sita = aco.calculate()
        sita = sita[:, 1:]
        aco.updatePheromone(px, py, sita)

    dis = aco.calDis(px, py)
    best_index = np.argmax(dis)
    

    last_x, last_y = 50, 100
    for path_x, path_y in zip(px[best_index, :], py[best_index, :]):
        dis += np.sqrt((path_x - last_x) ** 2 + (path_y - last_y) ** 2)
        last_x = path_x
        last_y = path_y
        print("=>", (int(path_x), int(path_y)))
    print("distance:", dis[best_index])
    time_end = time.time()
    print("time cost:", time_end - time_start, "s")
    map.draw_path(px[best_index, :], py[best_index, :])
    cv2.imshow("map", map.image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





def solve(solution):
    if solution.upper() == "GA":
        GASolve()
    elif solution.upper() == "DE":
        DESolve()
    elif solution.upper() == "PSO":
        PSOSolve()
    else:
        ACOSolve()