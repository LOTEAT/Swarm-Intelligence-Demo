import math
import numpy as np

def is_point_collide_to_circle(point1, center, r):
    return math.sqrt((point1[0] - center[0]) ** 2 + (point1[1] - center[1]) ** 2) <= r

def is_point_collide_to_rect(point1, center, width, height):
    x_min = center[0] - width / 2
    x_max = center[0] + width / 2
    y_min = center[1] - height / 2
    y_max = center[1] + height / 2
    return (x_min <= point1[0] <= x_max) and (y_min <= point1[1] <= y_max)



def is_collide_to_circle(point1, point2, center, r):
    points_x = np.linspace(point1[0], point2[0], 50)
    points_y = np.linspace(point1[1], point2[1], 50)
    for x, y in zip(points_x, points_y):
        if is_point_collide_to_circle((x, y), center, r):
            return True
    return False

    # A = point2[1] - point1[1]
    # B = point1[0] - point2[0]
    # C = point2[0] * point1[1] - point1[0] * point2[1]
    # dist = abs(A * center[0] + B * center[1] + C) / math.sqrt(A ** 2 + B ** 2 + 1e-15)
    # AO = [center[0] - point1[0], center[1] - point1[1]]
    # BO = [center[0] - point2[0], center[1] - point2[1]]
    # AB = [point2[0] - point1[0], point2[1] -point1[1]]
    # BA = [point1[0] - point2[0], point1[1] -point2[1]]
    # return dist <= r and (AO[0] * AB[0] + AO[1] * AB[1] >= 0) and (BO[0] * BA[0] + BO[1] * BA[1] >= 0)



def is_collide_to_rect(point1, point2, center, width, height):

    points_x = np.linspace(point1[0], point2[0], 50)
    points_y = np.linspace(point1[1], point2[1], 50)
    for x, y in zip(points_x, points_y):
        if is_point_collide_to_rect((x, y), center, width, height):
            return True
    return False


    # left_up = [center[0] - width / 2, center[1] - height / 2]
    # left_down = [center[0] - width / 2, center[1] + height / 2]
    # right_up = [center[0] + width / 2, center[1] - height / 2]
    # right_down = [center[0] + width / 2, center[1] + height / 2]
    # n1 = [point2[1] - point1[1], point1[0] - point2[0]]
    # n2 = [right_down[1] - left_up[1], left_up[0] - right_down[0]]
    # n3 = [right_up[1] - left_down[1], left_down[0] - right_up[0]]
    
    # dist_p1 = n1[0] * point1[0] + n1[1] * point1[1]
    # dist_left_up = n1[0] * left_up[0] + n1[1] * left_up[1]
    # dist_right_down = n1[0] * right_down[0] + n1[1] * right_down[1]
    # is_collision1 = (dist_left_up - dist_p1) * (dist_right_down - dist_p1) <= 0

    # dist_p1 = point1[0] * n2[0] + point2[1] * n2[1]
    # dist_p2 = point2[0] * n2[0] + point2[1] * n2[1]
    # dist_left_up = left_up[0] * n2[0] + left_up[1] * n2[1]
    # is_collision1 = is_collision1 and ((dist_p1 - dist_left_up) * (dist_p2 - dist_left_up) <= 0)



    # dist_p1 = n1[0] * point1[0] + n1[1] * point1[1]
    # dist_left_down = n1[0] * left_down[0] + n1[1] * left_down[1]
    # dist_right_up = n1[0] * right_up[0] + n1[1] * right_up[1]
    # is_collision2 = (dist_left_down - dist_p1) * (dist_right_up - dist_p1) <= 0

    # dist_p1 = point1[0] * n3[0] + point2[1] * n3[1]
    # dist_p2 = point2[0] * n3[0] + point2[1] * n3[1]
    # dist_left_down = left_down[0] * n3[0] + left_down[1] * n3[1]
    # is_collision2 = is_collision2 and ((dist_p1 - dist_left_down) * (dist_p2 - dist_left_down) <= 0)

    # return is_collision1 or is_collision2