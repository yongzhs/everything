# exercise of polar cordinate plot...
# https://matplotlib.org/3.1.0/gallery/mplot3d/surface3d.html
# https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html

import numpy as np
import matplotlib.pyplot as plt
import math

n_theta = 181
step_theta = 180/(n_theta - 1)
n_phi = 361
step_phi = 360/(n_phi - 1)
x = np.zeros([n_theta, n_phi], dtype = float)
y = np.zeros([n_theta, n_phi], dtype = float)
z = np.zeros([n_theta, n_phi], dtype = float)
for i in range(n_theta):
    for j in range(n_phi):
        x[i][j] = math.sin(i * step_theta * math.pi/180) * math.sin(i * step_theta * math.pi/180) * math.cos(j * step_phi * math.pi/180)
        y[i][j] = math.sin(i * step_theta * math.pi/180) * math.sin(i * step_theta * math.pi/180) * math.sin(j * step_phi * math.pi/180)
        z[i][j] = math.sin(i * step_theta * math.pi/180) * math.cos(i * step_theta * math.pi/180)
        
fig = plt.figure()
ax = fig.gca(projection = '3d')
surf = ax.plot_surface(x, y, z, cmap = plt.cm.coolwarm)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
fig.colorbar(surf) # , shrink = 0.5, aspect = 1
plt.show()