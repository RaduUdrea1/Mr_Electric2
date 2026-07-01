import numpy
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import constants
from scipy import integrate
x=np.linspace(-10,10,8)
y=np.linspace(-10,10,8)
z=np.linspace(-10,10,8)

X,Y,Z=np.meshgrid(x,y,z)
r=np.sqrt(x**2+y**2+z**2)
k=(1/(4*np.pi*constants.epsilon_0))
x0,y0,z0=(0,0,0)
rx=X-x0
ry=Y-y0
rz=Z-z0

q=float(input("Enter your charge in Coulombs!"))

Ex=k*q*(rx/r**3)
Ey=k*q*(ry/r**3)
Ez=k*q*(rz/r**3)

fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.quiver(X,Y,Z,Ex,Ey,Ez, length=1, normalize="False")
plt.gca().set_aspect('equal')
plt.show()



