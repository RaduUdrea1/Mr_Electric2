import matplotlib.pyplot as plt
import numpy as np
from scipy import constants


def One_charge():

    x=np.linspace(-10,10,8)
    y=np.linspace(-10,10,8)
    z=np.linspace(-10,10,8)

    X,Y,Z=np.meshgrid(x,y,z)

    k=(1/(4*np.pi*constants.epsilon_0))
    x0,y0,z0=(0,0,0)
    rx=X-x0
    ry=Y-y0
    rz=Z-z0
    r = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2)
    r_safe=np.maximum(r,1e-9)


    q=float(input("Enter your charge in Coulombs!"))

    Ex=k*q*(rx/r_safe**3)
    Ey=k*q*(ry/r_safe**3)
    Ez=k*q*(rz/r_safe**3)

    r_min=2.5
    ok=r>=r_min


    Emag=np.sqrt(Ex**2+Ey**2+Ez**2)
    if Emag.max()==0:
        print("There is no charge!")
        return
    scale=2

    Explot=Ex/Emag.max()*scale
    Eyplot=Ey/Emag.max()*scale
    Ezplot=Ez/Emag.max()*scale


    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    ax.quiver(X[ok],Y[ok],Z[ok],Explot[ok],Eyplot[ok],Ezplot[ok], length=4, normalize=False,)
    ax.scatter([0],[0],[0],color="Red",s=60)
    #plt.gca().set_aspect('equal')
    ax.set_box_aspect([1,1,1])
    ax.set_xlabel("x(m)")
    ax.set_ylabel("y(m)")
    ax.set_zlabel("z(m)")
    ax.set_title("Field of point charge q = " + str(q) + "(C)")
    plt.show()

def Two_charges():
    x=np.linspace(-50,50,10)
    y=np.linspace(-50,50,10)
    z=np.linspace(-50,50,10)
    q1 = float(input("Enter your first charge in Coulombs!"))
    q2 = float(input("Enter your second charge in Coulombs!"))
    l = float(input("Enter your distance!"))
    if l<=0:
        print("Distance must be positive!")
        return
    k = (1 / (4 * np.pi * constants.epsilon_0))

    (X,Y,Z)=np.meshgrid(x,y,z)
    (x1,y1,z1)=(-l/2,0,0)
    (x2,y2,z2)=(l/2,0,0)

    rx1=X-x1
    ry1=Y-y1
    rz1=Z-z1
    r1=np.sqrt(rx1**2+ry1**2+rz1**2)
    r1_safe=np.maximum(r1,1e-9)

    rx2=X-x2
    ry2=Y-y2
    rz2=Z-z2
    r2=np.sqrt(rx2**2+ry2**2+rz2**2)
    r2_safe=np.maximum(r2,1e-9)

    Ex1=k*q1*rx1/r1_safe**3
    Ey1=k*q1*ry1/r1_safe**3
    Ez1=k*q1*rz1/r1_safe**3

    Ex2=k*q2*rx2/r2_safe**3
    Ey2=k*q2*ry2/r2_safe**3
    Ez2=k*q2*rz2/r2_safe**3

    Ex=Ex1+Ex2
    Ey=Ey1+Ey2
    Ez=Ez1+Ez2

    r_min=12.5

    ok=(r1>=r_min)&(r2>=r_min)


    Emag = np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)
    if Emag.max()==0:
        print("There is no charge!")
        return
    scale = 10

    Explot = Ex / Emag.max() * scale
    Eyplot = Ey / Emag.max() * scale
    Ezplot = Ez / Emag.max() * scale
    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    ax.quiver(X[ok],Y[ok],Z[ok],Explot[ok],Eyplot[ok],Ezplot[ok], length=3, normalize=False)
    ax.scatter([x1,x2], [y1,y2], [z1,z2], color="Red", s=60)
    #plt.gca().set_aspect('equal')
    ax.set_box_aspect([1,1,1])
    ax.set_xlabel("x(m)")
    ax.set_ylabel("y(m)")
    ax.set_zlabel("z(m)")
    ax.set_title("Field of two point charges q1="+ str(q1)+"(C) and q2=" +str(q2)+ "(C), d=" +str(l))
    plt.show()

def One_chargeGauss():

    x=np.linspace(-10,10,8)
    y=np.linspace(-10,10,8)
    z=np.linspace(-10,10,8)


    X,Y,Z=np.meshgrid(x,y,z)

    k=(1/(4*np.pi*constants.epsilon_0))
    x0,y0,z0=(0,0,0)
    rx=X-x0
    ry=Y-y0
    rz=Z-z0
    r = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2)
    r_safe=np.maximum(r,1e-9)
    q=float(input("Enter your charge in Coulombs!"))

    Ex=k*q*(rx/r_safe**3)
    Ey=k*q*(ry/r_safe**3)
    Ez=k*q*(rz/r_safe**3)

    Emag = np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)
    if Emag.max()==0:
        print("There is no charge!")
        return
    scale = 2

    Explot = Ex / Emag.max() * scale
    Eyplot = Ey / Emag.max() * scale
    Ezplot = Ez / Emag.max() * scale

    sr = float(input("What radius of Gaussian Sphere would you like?"))
    if sr<=0:
        print("Sorry, choose a positive radius!")
        return

    q_enc = q
    flux = q_enc / constants.epsilon_0
    print("Enclosed charge is: " + str(q_enc) + "C")
    print("Electric flux is: " + str(flux) + "NM^2/C")

    Cx, Cy, Cz = (0.0, 0.0, 0.0)
    u=np.linspace(0,2*np.pi,48)
    v=np.linspace(0,np.pi,24)
    U,V=np.meshgrid(u,v)
    Xs=Cx+sr*np.sin(V)*np.cos(U)
    Ys=Cy+sr*np.sin(V)*np.sin(U)
    Zs=Cz+sr*np.cos(V)

    X0,Y0,Z0=(0,0,0)

    r_min=2.5
    ok=r>=r_min
    px = float(input("Enter your probe point (x)"))
    py = float(input("Enter your probe point (y)"))
    pz = float(input("Enter your probe point (z)"))

    prx = px - X0
    pry = py - Y0
    prz = pz - Z0
    pr = np.sqrt(prx ** 2 + pry ** 2 + prz ** 2)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(X[ok], Y[ok], Z[ok], Explot[ok], Eyplot[ok], Ezplot[ok], length=3, normalize=False)
    ax.scatter([0], [0], [0], color="Red", s=60)
    ax.plot_wireframe(Xs, Ys, Zs, color="cyan", linewidth=0.8, alpha=0.7, label="Gaussian Sphere")
    ax.set_box_aspect([1, 1, 1])

    if pr < 1e-9:
        print("Your probe is standing at the particle itself!")

    else:
        pEx = k * q * prx / pr ** 3
        pEy = k * q * pry / pr ** 3
        pEz = k * q * prz / pr ** 3
        pV = k * (q / pr)
        PEmag = np.sqrt(pEx ** 2 + pEy ** 2 + pEz ** 2)

        print("Your Voltage is " + str(pV))
        print("Electric field magnitude: " + str(PEmag))
        print(f"E=({pEx},{pEy},{pEz})N/C")

    if pr > 1e-9:
        ax.scatter([px], [py], [pz], color="green", s=80, label="Probe", zorder=10)

        ax.legend()

    ax.set_xlabel("x(m)")
    ax.set_ylabel("y(m)")
    ax.set_zlabel("z(m)")
    ax.set_title("Gaussian sphere of radius r="+ str(sr) +" around charge of "+ str(q)+ "(C)")

    plt.show()






def Dirac_Delta():
    n=12
    span=2.0
    x=np.linspace(-span,span,n)
    y=np.linspace(-span,span,n)
    z=np.linspace(-span,span,n)
    X,Y,Z=np.meshgrid(x,y,z)
    q=float(input("Enter your charge in Coulombs!"))

    dx, dy, dz =x[1]-x[0],y[1]-y[0],z[1]-z[0]
    dV=dx*dy*dz
    rho=np.zeros_like(X)
    i=np.argmin(np.abs(y-0))
    j=np.argmin(np.abs(x-0))
    kidx=np.argmin(np.abs(z-0))
    rho[i,j,kidx]=q/dV
    q_check=np.sum(rho)*dV
    print(f"∫ρ dV ≈ {q_check} C (should match q = {q})")


    k=(1/(4*np.pi*constants.epsilon_0))
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    r_safe = np.maximum(r, 1e-9)
    Ex = k * q * X / r_safe ** 3
    Ey = k * q * Y / r_safe ** 3
    Ez = k * q * Z / r_safe ** 3
    Emag = np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)
    if Emag.max()==0:
        print("There is no charge!")
        return
    R=1.2
    r_inner=0.15
    ok=(r>=r_inner)&(r<=R)
    scale = 0.8
    Explot=Ex/Emag.max()*scale
    Eyplot=Ey/Emag.max()*scale
    Ezplot=Ez/Emag.max()*scale



    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')

    ax.quiver(X[ok],Y[ok],Z[ok],Explot[ok],Eyplot[ok],Ezplot[ok], length=3, normalize=False)
    ax.scatter([0], [0], [0], color="Red", s=60)
    ax.set_xlabel("x(m)")
    ax.set_ylabel("y(m)")
    ax.set_zlabel("z(m)")
    ax.set_title("Schematic delta cluster at charge q="+str(q)+"(C)")
    plt.show()







print("Welcome to the electric field simulator! Possible representations are : (1) for the one charge electric field,"
      "(2) for the two charge electric field, (3) for the one charge and probe simulator, and (4) for the Dirac-Delta function! ")
initiation=int(input("What function would you like?"))
if initiation==1:
    One_charge()

elif initiation==2:
    Two_charges()

elif initiation==3:
    One_chargeGauss()

elif initiation==4:
    Dirac_Delta()
else:
    print("Inadequate Value")



