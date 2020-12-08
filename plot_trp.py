# this script reads data from a commercial TRP antenna test results and plot it... Python plot does not have good 3D plotting feature
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D

pin = 20
m = 11                                      # [15:15:165]
step_theta = 180 / (m + 1)
n = 24                                      # [0:15:345]
step_phi = 360 / n

data = pd.read_csv(r'C:\Users\yshao\Google Drive\Programming\python\b1_902.4MHz.txt')
d = data.values.tolist()
d = d[2:]                                               # remove first 2 elements 
eirp = [[0 for i in range(n + 1)] for j in range(m)]    # create an empty list 11 * 25
for i in range(m):
    for j in range(n):
        t = "".join(d[j * m + i])
        x = [float(j) for j in t.split()]
        eirp[i][j] = x[4]
    eirp[i][n] = eirp[i][0]     # copy the phi = 0 to phi = 360 since phi = 360 is not provided
    
x = np.zeros([m, n + 1], dtype = float)
y = np.zeros([m, n + 1], dtype = float)
z = np.zeros([m, n + 1], dtype = float)
r = np.zeros([m, n + 1], dtype = float)
for i in range(m):
    for j in range(n + 1): # add 1 to i because they start from theta = 15
        x[i][j] = eirp[i][j] * math.sin((i + 1) * step_theta * math.pi/180) * math.cos(j * step_phi * math.pi/180)
        y[i][j] = eirp[i][j] * math.sin((i + 1) * step_theta * math.pi/180) * math.sin(j * step_phi * math.pi/180)
        z[i][j] = eirp[i][j] * math.cos((i + 1) * step_theta * math.pi/180)
        r[i][j] = x[i][j]**2 + y[i][j]**2 + z[i][j]**2
        
# TODO color is mapped to z value, should map to amplitude
fig = plt.figure()
ax = fig.gca(projection = '3d')
surf = ax.plot_surface(x, y, z, cmap = plt.cm.jet)
ax.view_init(azim = 270, elev = 0)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Radiation pattern')
#fig.colorbar(surf)
plt.show()