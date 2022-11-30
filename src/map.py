import cv2
from config import MapConfig
import numpy as np
import time


class Map(MapConfig):
    def __init__(self):
        pass

    def draw_map(self):
        # drap map
        self.image=100 * np.ones((self.height,self.width,3),dtype=np.uint8)*255
        for shape in self.obstacle:
            if shape["shape"]=="rectangle":
                pt1=(shape["center"][0]-shape["width"]//2,shape["center"][0]-shape["height"]//2)
                pt2=(shape["center"][0]+shape["width"]//2,shape["center"][0]+shape["height"]//2)
                cv2.rectangle(self.image,pt1,pt2,0,thickness=-1)
            elif shape["shape"]=="circle":
                cv2.circle(self.image,shape["center"],shape["radius"],0,thickness=-1)
        
        self.map=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        _,self.map=cv2.threshold(self.map,125,255,cv2.THRESH_BINARY)
        cv2.circle(self.image,self.start,5,(255,0,0),thickness=2)
        cv2.circle(self.image,self.end,5,(0,255,0),thickness=2) 

    def draw_path(self, path_x, path_y):
        self.draw_map()
        for i in range(1, path_x.shape[0]):
            cv2.line(self.image, [int(path_x[i - 1]), int(path_y[i - 1])], [int(path_x[i]), int(path_y[i])], (255, 0, 255))

    def move(self, gen_x, gen_y):
        self.draw_map()
        size_x, size_y = gen_x.shape
        colors = np.random.randint(0, 255, size=(size_x, 3))

        for i in range(1, size_y):
            for j in range(size_x):
                x_split = np.linspace(gen_x[j][i - 1], gen_x[j][i], 10, endpoint=True)
                y_split = np.linspace(gen_y[j][i - 1], gen_y[j][i], 10, endpoint=True)
                
                for k in range(1, 10):
                    cv2.line(self.image, (int(x_split[k - 1]), int(y_split[k - 1])), (int(x_split[k]), int(y_split[k])), (int(colors[j, 0]), int(colors[j, 1]), int(colors[j, 2])), thickness=2)
                    cv2.line(self.image, (int(x_split[k - 1]), int(y_split[k - 1])), (int(x_split[k]), int(y_split[k])), (int(colors[j, 0]), int(colors[j, 1]), int(colors[j, 2])), thickness=2)

                    cv2.imshow("map", self.image)
                    cv2.waitKey(20)
        cv2.destroyAllWindows()



            


if __name__ == "__main__":
    map = Map()
    map.draw_map()
    cv2.imshow("map", map.image)
    cv2.waitKey(100000)



    