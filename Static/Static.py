import numpy as np


K=8.99e9
e0=8.854187817e-12
Q_ref=1e-9
R_ref=5.0
E_ref=K*Q_ref/(R_ref**2)

def scale_and_clip(Ex,Ey,Ez,scale=2.0,L_max=3):
    Explot=Ex/E_ref*scale
    Eyplot=Ey/E_ref*scale
    Ezplot=Ez/E_ref*scale

    L=np.sqrt(Explot**2+Eyplot**2+Ezplot**2)
    too_long=L>L_max

    if np.any(too_long):
        factor = L_max / L[too_long]
        Explot[too_long] *= factor
        Eyplot[too_long] *= factor
        Ezplot[too_long] *= factor
    return Explot, Eyplot, Ezplot

def one_charge(q, px, py, pz, n=8, span=100, r_min=12, scale=2.0):
    q = q * 1e-9
    x1d=np.linspace(-span,span,n)
    y1d=np.linspace(-span,span,n)
    z1d=np.linspace(-span,span,n)
    X,Y,Z=np.meshgrid(x1d,y1d,z1d)
    r=np.sqrt(X**2+Y**2+Z**2)
    r_safe = np.maximum(r, 1e-9)
    Ex=K*q*X/r_safe**3
    Ey=K*q*Y/r_safe**3
    Ez=K*q*Z/r_safe**3

    X0, Y0, Z0 = (0, 0, 0)
    prx = px - X0
    pry = py - Y0
    prz = pz - Z0

    pr = np.sqrt(prx ** 2 + pry ** 2 + prz ** 2)

    if pr < 1e-9:
        return {"ok": False, "message": "Your probe is at the charge point itself"}

    pEx = K * q * prx / pr ** 3
    pEy = K * q * pry / pr ** 3
    pEz = K * q * prz / pr ** 3

    Emag=np.sqrt(Ex**2+Ey**2+Ez**2)
    if Emag.max()==0:
        return{"ok":False,"message":"Electric Field is zero"}

    PEmag = np.sqrt(pEx ** 2 + pEy ** 2 + pEz ** 2)
    Explot, Eyplot, Ezplot = scale_and_clip(Ex, Ey, Ez)
    mask=r>=r_min
    c_vals = Emag[mask]

    return{
        "ok":True,
        "x":X[mask].tolist(),
        "y":Y[mask].tolist(),
        "z":Z[mask].tolist(),
        "u":Explot[mask].tolist(),
        "v":Eyplot[mask].tolist(),
        "w":Ezplot[mask].tolist(),
        "Ex": float(pEx),
        "Ey": float(pEy),
        "Ez": float(pEz),
        "Emag":float(PEmag),
        "px":float(px),
        "py":float(py),
        "pz":float(pz),
        "c": c_vals.tolist(),
        "cmin": float(np.percentile(c_vals, 5)),
        "cmax": float(np.percentile(c_vals, 95)),



    }

def two_charge(q1, q2, px, py, pz, l1, l2, l3, n=8, span=100, r_min=12, scale=2.0):
    x1d=np.linspace(-span,span,n)
    y1d = np.linspace(-span, span, n)
    z1d = np.linspace(-span, span, n)
    X, Y, Z = np.meshgrid(x1d, y1d, z1d)
    q1=q1*1e-9
    q2=q2*1e-9

    x1,y1,z1=(-l1/2,-l2/2,-l3/2)
    x2,y2,z2=(l1/2,l2/2,l3/2)

    totalDist=np.sqrt(l1**2+l2**2+l3**2)

    rx1 = X - x1
    ry1 = Y - y1
    rz1 = Z - z1
    r1 = np.sqrt(rx1 ** 2 + ry1 ** 2 + rz1 ** 2)
    r1_safe = np.maximum(r1, 1e-9)

    prx1=px-x1
    pry1=py-y1
    prz1=pz-z1

    prx2=px-x2
    pry2=py-y2
    prz2=pz-z2

    pr1=np.sqrt(prx1**2+pry1**2+prz1**2)
    pr2=np.sqrt(prx2**2+pry2**2+prz2**2)




    if pr1<1e-9 or pr2 <1e-9:
        return{"ok":False,"message":"Probe is at charge point"}

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


    pEx1 = K * q1 * prx1 / pr1 ** 3
    pEy1 = K * q1 * pry1 / pr1 ** 3
    pEz1 = K * q1 * prz1 / pr1 ** 3

    pEx2=K*q2*prx2/pr2**3
    pEy2=K*q2*pry2/pr2**3
    pEz2=K*q2*prz2/pr2**3

    pEx=pEx1+pEx2
    pEy=pEy1+pEy2
    pEz=pEz1+pEz2

    Explot, Eyplot, Ezplot = scale_and_clip(Ex, Ey, Ez)
    PEmag=np.sqrt(pEx**2+pEy**2+pEz**2)
    mask = (r1 >= r_min) & (r2>=r_min)
    c_vals = Emag[mask]
    return {
        "ok": True,
        "x": X[mask].tolist(),
        "y": Y[mask].tolist(),
        "z": Z[mask].tolist(),
        "u": Explot[mask].tolist(),
        "v": Eyplot[mask].tolist(),
        "w": Ezplot[mask].tolist(),
        "Ex": float(pEx),
        "Ey": float(pEy),
        "Ez": float(pEz),
        "Emag": float(PEmag),
        "px": float(px),
        "py": float(py),
        "pz": float(pz),
        "l1":float(l1),
        "l2":float(l2),
        "l3":float(l3),
        "c": c_vals.tolist(),
        "cmin": float(np.percentile(c_vals, 5)),
        "cmax": float(np.percentile(c_vals, 95)),

        "totalDist":float(totalDist),
    }
def One_chargeGauss(q, sr, px,py,pz, n=8, span=100, r_min=2.5, scale=12, Cx=0.0, Cy=0.0, Cz=0.0):
    q=q*1e-9
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
    Explot, Eyplot, Ezplot = scale_and_clip(Ex, Ey, Ez)
    mask = r >= r_min
    c_vals = Emag[mask]
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
        "pz": float (pz),
        "c": c_vals.tolist(),
        "cmin": float(np.percentile(c_vals, 5)),
        "cmax": float(np.percentile(c_vals, 95)),

    }
def Dirac_Delta(q, n=8, span=2):
    q=q*1e-9
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

    Explot, Eyplot, Ezplot = scale_and_clip(Ex, Ey, Ez)
    c_vals = Emag[ok]

    return{
        "ok": True,
        "x": X[ok].tolist(),
        "y": Y[ok].tolist(),
        "z": Z[ok].tolist(),
        "u": Explot[ok].tolist(),
        "v": Eyplot[ok].tolist(),
        "w": Ezplot[ok].tolist(),
        "q_check": float(q_check),
        "c": c_vals.tolist(),
        "cmin": float(np.percentile(c_vals, 5)),
        "cmax": float(np.percentile(c_vals, 95)),
    }

