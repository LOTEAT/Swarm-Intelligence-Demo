import numpy as np
from PSO.pso_config import PSOConfig
import random
import math
from utils import *


class PSO(PSOConfig):
    def __init__(self, obstacle):
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

    def init_velocity(self):
        vx = self.vmax * np.random.rand(self.population_size, self.dim)
        vy = self.vmax * np.random.rand(self.population_size, self.dim)
        return vx, vy

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
        return 1 / dis * records

    def fit_cmp(self, gen_x, gen_y, fitness_values, best_fit, best_pos_x, best_pos_y):
        best_index = np.argmax(fitness_values)
        best_fitness = fitness_values[best_index]
        best_x = gen_x[best_index, :]
        best_y = gen_y[best_index, :]
        for i in range(gen_x.shape[0]):
            if fitness_values[i] > best_fit[i]:
                best_pos_x[i, :] = gen_x[i, :]
                best_pos_y[i, :] = gen_y[i, :]
                best_fit[i] = fitness_values[i] 
        return best_fit, best_pos_x, best_pos_y, best_fitness, best_x, best_y



    def update_velocity(self, vx, vy, gen_x, gen_y, best_pos_x, best_pos_y, best_x, best_y):
        new_vx = self.w * vx + (self.c1 * random.random() * (best_pos_x - gen_x) + self.c2 * random.random() * (best_x - gen_x))[:, 1:-1]
        new_vy = self.w * vy + (self.c1 * random.random() * (best_pos_y - gen_y) + self.c2 * random.random() * (best_y - gen_y))[:, 1:-1]
        return new_vx, new_vy

    
    def update_pos(self, gen_x, gen_y, vx, vy):
        gen_x[:, 1:-1] += vx
        gen_y[:, 1:-1] += vy
        return gen_x, gen_y