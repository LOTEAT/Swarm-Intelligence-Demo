import numpy as np
from GA.ga_config import GAConfig
import random
import math
from utils import *

# generic algorithm
class GA(GAConfig):
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

    def calFitness(self, gen_x, gen_y, records):
        size_x, size_y = gen_x.shape
        dis = np.zeros(size_x)
        for i in range(size_x):
            for j in range(size_y - 1):
                dis[i] += math.sqrt((gen_x[i, j] - gen_x[i, j + 1]) ** 2 + (gen_y[i, j] - gen_y[i, j + 1]) ** 2)
        return np.exp(150 / dis * records) - 1


    def select(self, gen_x, gen_y, fitness_value):
        size_x, size_y = gen_x.shape
        new_gen_x = np.zeros(gen_x.shape)
        new_gen_y = np.zeros(gen_y.shape)
        for i in range(size_x):
            mask = np.random.rand(size_x) >= 0.3
            best_index = np.argmax(fitness_value[mask])
            new_gen_x[i, :] = gen_x[best_index, :]
            new_gen_y[i, :] = gen_y[best_index, :]
        return new_gen_x, new_gen_y


    def cross_over(self, gen_x, gen_y, fitness_value):
        best_index = np.argmax(fitness_value)
        size_x, size_y = gen_x.shape
        new_gen_x = gen_x.copy()
        new_gen_y = gen_y.copy()
        new_gen_x[0, :] = gen_x[best_index, :]
        new_gen_y[0, :] = gen_y[best_index, :]
        gen_x[0, :], gen_x[best_index, :] = gen_x[best_index, :], gen_x[0, :]
        gen_y[0, :], gen_y[best_index, :] = gen_y[best_index, :], gen_y[0, :]
        for i in range(1, size_x - 1, 2):
            p = random.random()
            if p <= self.pa:
                cross_ratio = random.random()
                new_gen_x[i, :] = cross_ratio * gen_x[i, :] + (1 - cross_ratio) * gen_x[i + 1, :]
                new_gen_y[i, :] = cross_ratio * gen_y[i, :] + (1 - cross_ratio) * gen_y[i + 1, :]
                new_gen_x[i + 1, :] = cross_ratio * gen_x[i + 1, :] + (1 - cross_ratio) * gen_x[i, :]
                new_gen_y[i + 1, :] = cross_ratio * gen_y[i + 1, :] + (1 - cross_ratio) * gen_y[i, :]
            else:
                new_gen_x[i, :] = gen_x[i, :]
                new_gen_y[i, :] = gen_y[i, :]
                new_gen_x[i + 1, :] = gen_x[i + 1, :]
                new_gen_y[i + 1, :] = gen_y[i + 1, :]
        return new_gen_x, new_gen_y

    def mutate(self, gen_x, gen_y, fitness_value):
        best_index = np.argmax(fitness_value)
        best_index = np.argmax(fitness_value)
        size_x, size_y = gen_x.shape
        new_gen_x = np.zeros(gen_x.shape)
        new_gen_y = np.zeros(gen_y.shape)
        new_gen_x[0, :] = gen_x[best_index, :]
        new_gen_y[0, :] = gen_y[best_index, :]
        gen_x[0, :], gen_x[best_index, :] = gen_x[best_index, :], gen_x[0, :]
        gen_y[0, :], gen_y[best_index, :] = gen_y[best_index, :], gen_y[0, :]


        for i in range(1, size_x):
            p = random.random()
            if p < self.pc:
                for j in range(1, size_y - 1):
                    mutation_x = self.x_min + (self.x_max - self.x_min) * random.random()
                    mutation_y = self.y_min + (self.y_max - self.y_min) * random.random()
                    while self.pointCollison(mutation_x, mutation_y):
                        mutation_x = self.x_min + (self.x_max - self.x_min) * random.random()
                        mutation_y = self.y_min + (self.y_max - self.y_min) * random.random()
                    new_gen_x[i, j] = mutation_x
                    new_gen_y[i, j] = mutation_y

            else:
                new_gen_x[i, :] = gen_x[i, :]
                new_gen_y[i, :] = gen_y[i, :]
        new_gen_x[:, 0], new_gen_y[:, 0] = self.start_x, self.start_y
        new_gen_x[:, -1], new_gen_y[:, -1] = self.end_x, self.end_y
        return new_gen_x, new_gen_y



