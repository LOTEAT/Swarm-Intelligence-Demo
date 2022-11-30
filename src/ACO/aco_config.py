from math import pi
import numpy as np
from config import SolverConfig

class ACOConfig(SolverConfig):
    NC = 10
    m = 200
    tij_ori = 1000
    p = 0.01
    tlim = [0, 1000]
    a = 1
    b = 3
    sitaran = [0, pi/4, pi/2, 3/4*pi, pi, 5/4*pi, 3/2*pi, 7/4*pi, 2*pi]
    precision = 50
    enx = int(SolverConfig.x_max/precision)
    eny = int(SolverConfig.y_max/precision)
    tij = tij_ori * np.ones((int(enx), int(eny), 8))
    nij = np.zeros((int(enx), int(eny), 8))


