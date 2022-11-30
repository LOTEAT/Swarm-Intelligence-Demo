import numpy as np
from DE.de_config import DEConfig
import random
import math
from utils import *

class DE(DEConfig):
    def __init__(self, obstacle):
        # obstacles
        self.obstacle = obstacle

    def pointCollison(self, x, y):
        # judge whether a point collides with the obstacle.
        is_collision = False
        for each_obstacle in self.obstacle:
            if each_obstacle["shape"] == "circle":
                is_collision = is_point_collide_to_circle([x, y], each_obstacle["center"], each_obstacle["radius"])
            elif each_obstacle["shape"] == "rectangle":
                is_collision = is_point_collide_to_rect([x, y], each_obstacle["center"], each_obstacle["width"], each_obstacle["height"])
            if is_collision:
                return is_collision
        return is_collision
    
    def generate_random_point(self):
        # get two random points
        cur_x = self.x_min + (self.x_max - self.x_min) * random.random()
        cur_y = self.y_min + (self.y_max - self.y_min) * random.random()
        return cur_x, cur_y

    def init_generation(self):
        # init population
        gen_x = np.zeros((self.population_size, self.dim + 2))
        gen_y = np.zeros((self.population_size, self.dim + 2))
        for i in range(self.population_size):
            for j in range(self.dim + 2):
                cur_x, cur_y = self.generate_random_point()
                while self.pointCollison(cur_x, cur_y):
                    cur_x, cur_y = self.generate_random_point()
                gen_x[i, j] = cur_x
                gen_y[i, j] = cur_y
        gen_x[:, 0] = self.start_x
        gen_x[:, -1] = self.end_x
        gen_y[:, 0] = self.start_y
        gen_y[:, -1] = self.end_y
        return gen_x, gen_y

    def lineCollision(self, gen_x, gen_y):  
        size_x, size_y = gen_x.shape
        records = np.ones(size_x)
        for i in range(size_x):
            for j in range(size_y - 1):
                if (gen_x[i, j] == gen_x[i, j + 1]) and (gen_y[i, j] == gen_y[i, j + 1]):
                    continue
                if(records[i] == 0):
                    break
                for each_obstacle in self.obstacle:
                    if each_obstacle["shape"] == "circle":
                        flag = is_collide_to_circle([gen_x[i, j], gen_y[i, j]], [gen_x[i, j + 1], gen_y[i, j + 1]],each_obstacle["center"], each_obstacle["radius"])
                    if each_obstacle["shape"] == "rectangle":
                        flag = is_collide_to_rect([gen_x[i, j], gen_y[i, j]], [gen_x[i, j + 1], gen_y[i, j + 1]], each_obstacle["center"], each_obstacle["width"], each_obstacle["height"])
                    if flag:
                        records[i] = 0
                        break
        return records

    def mutate(self, gen_x, gen_y):
        gen_x_mutation = np.zeros(gen_x.shape)
        gen_y_mutation = np.zeros(gen_y.shape)
        size_x, size_y = gen_x.shape
        for i in range(gen_x.shape[0]):
            r1 = random.randint(0, size_x - 1)
            r2 = random.randint(0, size_x - 1)
            r3 = random.randint(0, size_x - 1)
            while r1 == i or r2 == i or r3 == i or r1 == r2 or r2 == r3 or r1 == r3:
                r1 = random.randint(0, size_x - 1)
                r2 = random.randint(0, size_x - 1)
                r3 = random.randint(0, size_x - 1)
            gen_x_mutation[i, :] = gen_x[r1, :] + self.F * (gen_x[r2, :] - gen_x[r3, :])
            gen_y_mutation[i, :] = gen_y[r1, :] + self.F * (gen_y[r2, :] - gen_y[r3, :])
        return gen_x_mutation, gen_y_mutation

    def cross_over(self, gen_x, gen_y, gen_x_mutation, gen_y_mutation):
        gen_x_crossover = np.zeros(gen_x.shape)
        gen_y_crossover = np.zeros(gen_y.shape)
        size_x, size_y = gen_x.shape
        for i in range(size_x):
            for j in range(size_y):
                p = random.random()
                if p <= self.cr:
                    gen_x_crossover[i, j] = gen_x_mutation[i, j]
                    gen_y_crossover[i, j] = gen_y_mutation[i, j]
                else:
                    gen_x_crossover[i, j] = gen_x[i, j]
                    gen_y_crossover[i, j] = gen_y[i, j]
        return gen_x_crossover, gen_y_crossover
    
    def CalculateFitness(self, gen_x, gen_y, records):
        size_x, size_y = gen_x.shape
        dis = np.zeros(size_x)
        for i in range(size_x):
            for j in range(size_y - 1):
                dis[i] += math.sqrt((gen_x[i, j] - gen_x[i, j + 1]) ** 2 + (gen_y[i, j] - gen_y[i, j + 1]) ** 2)
        return np.exp(150 / dis * records) - 1



    def select(self, gen_x, gen_y, gen_x_crossover, gen_y_crossover):
        records = self.lineCollision(gen_x_crossover, gen_y_crossover)
        crossover_fitness = self.CalculateFitness(gen_x_crossover, gen_y_crossover, records)
        records = self.lineCollision(gen_x, gen_y)
        fitness = self.CalculateFitness(gen_x, gen_y, records)
        new_gen_x = np.zeros(gen_x_crossover.shape)
        new_gen_y = np.zeros(gen_y_crossover.shape)
        for i in range(self.population_size):
            if fitness[i] > crossover_fitness[i]:
                new_gen_x[i] = gen_x[i]
                new_gen_y[i] = gen_y[i]
            else:
                new_gen_x[i] = gen_x_crossover[i]
                new_gen_y[i] = gen_y_crossover[i]
        return new_gen_x, new_gen_y
    	




	


    