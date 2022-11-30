import matplotlib.pyplot as plt
import numpy as np

x = [100, 300, 400, 500, 600, 700, 800, 900, 1000]
y1 = [81.09, 293.31, 380.59, 418.94, 533.68, 568.34, 694.19, 866.49, 925.07]
y2 = [628.92, 466.01, 466.00, 480.28, 465.99, 465.99, 465.98, 465.98, 480.21]


fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1_l = ax1.plot(x, y1, label="time")
ax1.set_ylabel('time')
ax1.legend(loc="upper left")

ax2 = ax1.twinx()  # this is the important function
ax2_l = ax2.plot(x, y2, 'r', label="distance")
ax2.set_ylabel('distance')
ax2.set_xlabel('iterations')
ax2.legend(loc=0)


plt.show()
