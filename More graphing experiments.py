import numpy as np
import matplotlib.pyplot as plt
import flask


x=np.linspace(-10,10,12)
y=np.linspace(-10,10,12)
X,Y=np.meshgrid(x,y)

r2=X**2+Y**2
U=X**2/r2
V=Y**2/r2
dU_dy,dU_dx = np.gradient(U,x,y)
dV_dy,dV_dx = np.gradient(V,x,y)
divergence=dU_dx+dV_dy






fig=plt.figure()
#ax=fig.add_subplot(111,projection='3d')

plt.contourf(X,Y,divergence,cmap='RdBu_r')

plt.colorbar(label='divergence')
plt.quiver(X,Y,U,V)
plt.show()


