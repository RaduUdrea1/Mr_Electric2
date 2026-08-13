import numpy as np

K=8.99e9
e0=8.854187817e-12
def one_charge(q, n=8, span=10, r_min=2.5, scale=2.0):
    x1d=np.linspace(-span,span,n)
    y1d=np.linspace(-span,span,n)
    z1d=np.linspace(-span,span,n)
    X,Y,Z=np.meshgrid(x1d,y1d,z1d)
    r=np.sqrt(X**2+Y**2+Z**2)
    r_safe=np.maximum(r,1e-9)
    Ex=K*q*X/r_safe**3
    Ey=K*q*Y/r_safe**3
    Ez=K*q*Z/r_safe**3

    Emag=np.sqrt(Ex**2+Ey**2+Ez**2)
    if Emag.max()==0:
        return{"ok":False,"message":"Electric Field is zero"}

    Explot=Ex/Emag.max()*scale
    Eyplot=Ey/Emag.max()*scale
    Ezplot=Ez/Emag.max()*scale

    mask=r>=r_min
    return{
        "ok":True,
        "x":X[mask].tolist(),
        "y":Y[mask].tolist(),
        "z":Z[mask].tolist(),
        "u":Explot[mask].tolist(),
        "v":Eyplot[mask].tolist(),
        "w":Ezplot[mask].tolist(),


    }

def two_charge(q1, q2, l, n=8, span=10, r_min=2.5, scale=2.0):
    x1d=np.linspace(-span,span,n)
    y1d = np.linspace(-span, span, n)
    z1d = np.linspace(-span, span, n)
    X, Y, Z = np.meshgrid(x1d, y1d, z1d)

    x1,y1,z1=(-l/2,0,0)
    x2,y2,z2=(l/2,0,0)

    rx1 = X - x1
    ry1 = Y - y1
    rz1 = Z - z1
    r1 = np.sqrt(rx1 ** 2 + ry1 ** 2 + rz1 ** 2)
    r1_safe = np.maximum(r1, 1e-9)

    rx2 = X - x2
    ry2 = Y - y2
    rz2 = Z - z2
    r2 = np.sqrt(rx2 ** 2 + ry2 ** 2 + rz2 ** 2)
    r2_safe = np.maximum(r2, 1e-9)

    Ex1 = K * q1 * rx1 / r1_safe ** 3
    Ey1 = K * q1 * ry1 / r1_safe ** 3
    Ez1 = K * q1 * rz1 / r1_safe ** 3

    Ex2=K*q2*rx2/r2_safe**3
    Ey2=K*q2*ry2/r2_safe**3
    Ez2=K*q2*rz2/r2_safe**3

    Ex=Ex1+Ex2
    Ey=Ey1+Ey2
    Ez=Ez1+Ez2


    Emag = np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)
    if Emag.max() == 0:
        return {"ok": False, "message": "Electric Field is zero"}

    Explot = Ex / Emag.max() * scale
    Eyplot = Ey / Emag.max() * scale
    Ezplot = Ez / Emag.max() * scale

    mask = (r1 >= r_min) & (r2>=r_min)
    return {
        "ok": True,
        "x": X[mask].tolist(),
        "y": Y[mask].tolist(),
        "z": Z[mask].tolist(),
        "u": Explot[mask].tolist(),
        "v": Eyplot[mask].tolist(),
        "w": Ezplot[mask].tolist(),

    }
def One_chargeGauss(q, sr, px,py,pz, n=8, span=10, r_min=2.5, scale=2.0, Cx=0.0, Cy=0.0, Cz=0.0):
    x1d = np.linspace(-span, span, n)
    y1d = np.linspace(-span, span, n)
    z1d = np.linspace(-span, span, n)
    X, Y, Z = np.meshgrid(x1d, y1d, z1d)
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    r_safe = np.maximum(r, 1e-9)
    Ex = K * q * X / r_safe ** 3
    Ey = K * q * Y / r_safe ** 3
    Ez = K * q * Z / r_safe ** 3

    Emag = np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)

    if Emag.max() == 0:
        return {"ok": False, "message": "Electric Field is zero"}
    if sr <=0:
        return{"ok": False, "message": "Sr should be a positive number"}

    Explot = Ex / Emag.max() * scale
    Eyplot = Ey / Emag.max() * scale
    Ezplot = Ez / Emag.max() * scale
    q_enc = q
    flux = q_enc / e0
    u=np.linspace(0,2*np.pi,48)
    v=np.linspace(0,np.pi,24)
    U,V=np.meshgrid(u,v)
    Xs=Cx+sr*np.sin(V)*np.cos(U)
    Ys=Cy+sr*np.sin(V)*np.sin(U)
    Zs=Cz+sr*np.cos(V)
    X0,Y0,Z0=(0,0,0)
    prx=px-X0
    pry=py-Y0
    prz=pz-Z0


    pr=np.sqrt(prx ** 2 + pry ** 2 + prz ** 2)

    if pr<1e-9:
        return {"ok": False, "message": "Your probe is at the charge point itself"}

    pEx = K * q * prx / pr ** 3
    pEy = K * q * pry / pr ** 3
    pEz = K * q * prz / pr ** 3
    pV = K * (q / pr)
    PEmag = np.sqrt(pEx ** 2 + pEy ** 2 + pEz ** 2)

    mask = r >= r_min
    return {
        "ok": True,
        "x": X[mask].tolist(),
        "y": Y[mask].tolist(),
        "z": Z[mask].tolist(),
        "u": Explot[mask].tolist(),
        "v": Eyplot[mask].tolist(),
        "w": Ezplot[mask].tolist(),
        "flux": float (flux),
        "V":float (pV),
        "Emag": float (PEmag),
        "Ex": float (pEx),
        "Ey": float (pEy),
        "Ez": float (pEz),
        "Xs":Xs.ravel().tolist(),
        "Ys":Ys.ravel().tolist(),
        "Zs":Zs.ravel().tolist(),
        "px":float (px),
        "py":float (py),
        "pz": float (pz)

    }
def Dirac_Delta(q, n=12, span=2.0):
    x1d = np.linspace(-span, span, n)
    y1d = np.linspace(-span, span, n)
    z1d = np.linspace(-span, span, n)
    X, Y, Z = np.meshgrid(x1d, y1d, z1d)

    dx,dy,dz=(x1d[1]-x1d[0],y1d[1]-y1d[0],z1d[1]-z1d[0])
    dV=dx*dy*dz
    rho=np.zeros_like(X)
    i = np.argmin(np.abs(y1d - 0))
    j = np.argmin(np.abs(x1d - 0))
    kidx = np.argmin(np.abs(z1d - 0))
    rho[i, j, kidx] = q / dV
    q_check = np.sum(rho) * dV


    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    r_safe = np.maximum(r, 1e-9)
    Ex = K * q * X / r_safe ** 3
    Ey = K * q * Y / r_safe ** 3
    Ez = K * q * Z / r_safe ** 3
    Emag = np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)

    if Emag.max() == 0:
        return {"ok": False, "message": "Electric Field is zero"}


    R=1.2
    r_inner=0.15
    ok=(r>=r_inner)&(r<=R)
    scale = 0.8
    Explot=Ex/Emag.max()*scale
    Eyplot=Ey/Emag.max()*scale
    Ezplot=Ez/Emag.max()*scale


    return{
        "ok": True,
        "x": X[ok].tolist(),
        "y": Y[ok].tolist(),
        "z": Z[ok].tolist(),
        "u": Explot[ok].tolist(),
        "v": Eyplot[ok].tolist(),
        "w": Ezplot[ok].tolist(),
        "q_check": float(q_check),
    }

