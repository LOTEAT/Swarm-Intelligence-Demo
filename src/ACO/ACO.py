import numpy as np
from ACO.aco_config import ACOConfig
import random
from utils import *


class ACO(ACOConfig):
    
    def __init__(self, obstacle):
        self.obstacle = obstacle
        self.obs = np.zeros((int(self.enx + 1), int(self.eny + 1)))
        self.nij[:, :, 0: 9: 2] = self.precision * np.ones((self.enx, self.eny, 4))
        self.nij[:, :, 1: 9: 2] = np.sqrt(2) * self.precision * np.ones((self.enx, self.eny, 4))

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



    def select(self, fitvalue):
        totalfit = np.sum(fitvalue)
        p_fitvalue = fitvalue / totalfit
        p_fitvalue = np.cumsum(p_fitvalue)

        rand = random.random()
        selection = 0
        for i in range(p_fitvalue.shape[0]):
            if rand < p_fitvalue[i]:
                selection = i
                break
        return selection

    def IFunction(self, x):
        if x > 0:
            return 1
        elif x == 0:
            return 0
        else:
            return -1

    def lineCollision(self, point1, point2):  

        for each_obstacle in self.obstacle:
            if each_obstacle["shape"] == "circle":
                flag = is_collide_to_circle(point1, point2, each_obstacle["center"], each_obstacle["radius"])
            if each_obstacle["shape"] == "rectangle":
                flag = is_collide_to_rect(point1, point2, each_obstacle["center"], each_obstacle["width"], each_obstacle["height"])
            if flag:
                return True
        return False


    def calculate(self):
        px = np.zeros((self.m, 1))
        py = np.zeros((self.m, 1))
        px[:, 0] = self.start_x
        py[:, 0] = self.start_y
        theta = np.zeros((self.m, 1))
        while True:
            gen_x = (px[:, -1] == self.end_x * np.ones(1)) 
            gen_y = (py[:, -1] == self.end_y * np.ones(1))

            if np.sum(gen_x) + np.sum(gen_y) == 2 * self.m:
                break
            theta = np.hstack((theta, np.zeros((self.m, 1))))
            px = np.hstack((px, np.zeros((self.m, 1))))
            py = np.hstack((py, np.zeros((self.m, 1))))



            for i in range(self.m):
                while True:
                    if px[i, -2] == self.end_x and py[i, -2] == self.end_y:
                        px[i, -1] = px[i, -2]
                        py[i, -1] = py[i, -2]
                        theta[i, -1] = theta[i, -2]
                        break
                    
                    lasttx = int(px[i, -2] / self.precision)
                    lastty = int(py[i, -2] / self.precision)

                    ttij = self.tij[lasttx, lastty, :].reshape((1, 8))
                    nnij = self.nij[lasttx, lastty, :].reshape((1, 8))
                    
  
                    
                    pij = ttij * nnij / np.sum(ttij * nnij)
                    next_theta = int(self.select(pij))
                    
                    

                    ppx = px[i, -2] + self.precision * self.IFunction(np.cos(self.sitaran[next_theta]))
                    ppy = py[i, -2] + self.precision * self.IFunction(np.sin(self.sitaran[next_theta]))
                    
                    # for j in range(px[i, :].shape[0]):
                    #     if px[i, j] == ppx and py[i, j] == ppy:
                    #         flag1 = False
                    #         break
                    
                    # ab = np.vstack((px[i, :], py[i, :]))
                    # abc = np.vstack((ppx, ppy))

                    # for mt in range(ab.shape[1]):
                    #     flag = np.sum(ab[:, mt] - abc)
                    #     if flag == 0:
                    #         print(i)
                    #         break
                    flag = self.lineCollision((px[i, -2], py[i, -2]), (ppx, ppy))

                    

                    if ppx > self.x_min and ppy > self.y_min and ppx < self.x_max and ppy < self.y_max and not flag:
                        tx = int(ppx / self.precision)
                        ty = int(ppy / self.precision)
                        if self.obs[tx, ty] == 0:
                            px[i, -1] = ppx
                            py[i, -1] = ppy
                            theta[i, -1] = next_theta
                            break
                    
                        
        return px, py, theta

    def calDis(self, px, py):
        distance = np.zeros(px.shape[0])
        for i in range(px.shape[0]):
            dist = 0
            for j in range(px.shape[1] - 1):
                dist += np.sqrt((px[i, j+1]-px[i, j]) ** 2 + (py[i, j+1] - py[i, j]) ** 2)
            distance[i] = dist
        return distance


    def updatePheromone(self, px, py, theta):
        distance = self.calDis(px, py)
        minindex = np.argmin(distance)
        mindis = distance[minindex]
        bestpx = px[minindex, :]
        bestpy = py[minindex, :]
        best_theta = theta[minindex, :]
        delta = 1 / mindis
        size_x, size_y = px.shape
        deltaij = np.zeros(self.tij.shape)
        for i in range(size_x):
            for j in range(size_y - 1):
                ttx = bestpx == px[i, j]
                tty = bestpy == py[i, j]
                tttheta = best_theta == theta[i, j]
                flag = ttx.any() and tty.any() and tttheta.any()
                if not flag:
                    tx = px[i, j] / self.precision
                    ty = py[i, j] / self.precision 
                    deltaij[int(tx), int(ty), int(theta[i, j])] += delta
        
        self.tij = (1 - self.p) * self.tij + deltaij

        a, b, c = self.tij.shape

        for i in range(a):
            for j in range(b):
                for k in range(c):
                    if np.isnan(self.tij[i, j, k]):
                        self.tij[i, j, k] = 1000
                    elif self.tij[i, j, k] > 1000:
                        self.tij[i, j, k] = 1000
                    elif self.tij[i, j, k] < 0:
                        self.tij[i, j, k] = 0
                    else:
                        self.tij[i, j, k] = self.tij[i, j, k]




    
    def set_obstacle(self):
        for i in range(self.enx + 1):
            for j in range(self.eny + 1):
                x = i * self.precision
                y = j * self.precision
                if self.pointCollison(x, y):
                    self.obs[i][j] = 1
    

                


