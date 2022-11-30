from map import Map
from GA.GA import GA
from DE.DE import DE
import cv2
import numpy as np



def get_best(best_fitness, fitness, gen_x, gen_y, best_path_x, best_path_y):
    best_index = np.argmax(fitness)
    if fitness[best_index] > best_fitness:
        best_fitness = fitness[best_index]
        best_path_x = gen_x[best_index, :]
        best_path_y = gen_y[best_index, :]
    return best_fitness, best_path_x, best_path_y


if __name__ == "__main__":
    map = Map()
    map.draw_map()

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
        map.move(gen_x, gen_y)

    map.draw_path(best_path_x, best_path_y)


    # map.move(gen_x, gen_y)
    cv2.destroyAllWindows()



