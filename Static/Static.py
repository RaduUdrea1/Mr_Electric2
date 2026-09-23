import numpy as np



K=8.99e9
e0=8.854187817e-12
Q_ref=1e-9
R_ref=5.0
E_ref=K*Q_ref/(R_ref**2)

def scale_and_clip(Ex,Ey,Ez,scale=2.0,L_max=1.0, adapt=0.5):
    Emag=np.sqrt(Ex**2+Ey**2+Ez**2)
    positive=Emag[Emag>0]
    if positive.size==0:
        return Ex*0, Ey*0, Ez*0
    e_local=float(np.percentile(positive,90))
    if e_local < 1e-30:
        e_local=1e-30

    e_ref=(e_local**adapt)*(E_ref**(1.0-adapt))

    Explot=Ex/e_ref*scale
    Eyplot=Ey/e_ref*scale
    Ezplot=Ez/e_ref*scale

    L=np.sqrt(Explot**2+Eyplot**2+Ezplot**2)
    too_long=L>L_max

    if np.any(too_long):
        factor = L_max / L[too_long]
        Explot[too_long] *= factor
        Eyplot[too_long] *= factor
        Ezplot[too_long] *= factor
    return Explot, Eyplot, Ezplot

def one_charge(q, x,y,z , px, py, pz, n=8, span=100, r_min=12, scale=2.0):
    q = q * 1e-9
    x1d=np.linspace(-span,span,n)
    y1d=np.linspace(-span,span,n)
    z1d=np.linspace(-span,span,n)
    X,Y,Z=np.meshgrid(x1d,y1d,z1d)
    rx=X-x
    ry=Y-y
    rz=Z-z
    r=np.sqrt(rx**2+ry**2+rz**2)
    r_safe = np.maximum(r, 1e-9)
    Ex=K*q*rx/r_safe**3
    Ey=K*q*ry/r_safe**3
    Ez=K*q*rz/r_safe**3



    prx = px - x
    pry = py - y
    prz = pz - z

    pr = np.sqrt(prx ** 2 + pry ** 2 + prz ** 2)
    pV = K * q / pr

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
        "qx":float(x),
        "qy":float(y),
        "qz":float(z),
        "px":float(px),
        "py":float(py),
        "pz":float(pz),
        "c": c_vals.tolist(),
        "cmin": float(np.percentile(c_vals, 5)),
        "cmax": float(np.percentile(c_vals, 95)),
        "V":float(pV),



    }

def two_charge(q1, q2, px, py, pz, x1, y1, z1, x2,y2,z2 , n=8, span=100, r_min=12, scale=2.0):
    x1d=np.linspace(-span,span,n)
    y1d = np.linspace(-span, span, n)
    z1d = np.linspace(-span, span, n)
    X, Y, Z = np.meshgrid(x1d, y1d, z1d)
    q1=q1*1e-9
    q2=q2*1e-9
    lx=(x2-x1)
    ly=(y2-y1)
    lz=(z2-z1)

    totalDist=np.sqrt(lx**2+ly**2+lz**2)

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

    pV = K * q1 / pr1 + K * q2 / pr2
    U = K * q1 * q2 / totalDist
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
        "x1":float(x1),
        "y1":float(y1),
        "z1":float(z1),
        "x2":float(x2),
        "y2":float(y2),
        "z2":float(z2),
        "lx":float(lx),
        "ly":float(ly),
        "lz":float(lz),
        "c": c_vals.tolist(),
        "cmin": float(np.percentile(c_vals, 5)),
        "cmax": float(np.percentile(c_vals, 95)),
        "totalDist":float(totalDist),
        "V":float(pV),
        "U":float(U),
    }
def One_chargeGauss(q,x,y,z, sr, px,py,pz, n=8, span=100, r_min=12, Cx=0.0, Cy=0.0, Cz=0.0):
    q=q*1e-9
    x1d = np.linspace(-span, span, n)
    y1d = np.linspace(-span, span, n)
    z1d = np.linspace(-span, span, n)
    X, Y, Z = np.meshgrid(x1d, y1d, z1d)
    rx=X-x
    ry=Y-y
    rz=Z-z
    r = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2)
    r_safe = np.maximum(r, 1e-9)
    Ex = K * q * rx / r_safe ** 3
    Ey = K * q * ry / r_safe ** 3
    Ez = K * q * rz / r_safe ** 3

    Emag = np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)

    if Emag.max() == 0:
        return {"ok": False, "message": "Electric Field is zero"}
    if sr <=0:
        return{"ok": False, "message": "Sr should be a positive number"}

    Cx,Cy,Cz=0.0,0.0,0.0
    r_from_center=np.sqrt((x-Cx)**2+(y-Cy)**2+(z-Cz)**2)
    if r_from_center<sr:
        q_enc=q
    else:
        q_enc=0.0

    flux=q_enc/e0


    u=np.linspace(0,2*np.pi,48)
    v=np.linspace(0,np.pi,24)
    U,V=np.meshgrid(u,v)
    Xs=Cx+sr*np.sin(V)*np.cos(U)
    Ys=Cy+sr*np.sin(V)*np.sin(U)
    Zs=Cz+sr*np.cos(V)

    prx=px-x
    pry=py-y
    prz=pz-z


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
        "qx":float(x),
        "qy":float(y),
        "qz":float(z),
        "px":float (px),
        "py":float (py),
        "pz": float (pz),
        "c": c_vals.tolist(),
        "cmin": float(np.percentile(c_vals, 5)),
        "cmax": float(np.percentile(c_vals, 95)),
        "q_enc":float(q_enc),
        "inside":bool(r_from_center<sr),
        "Cx":float(Cx),
        "Cy":float(Cy),
        "Cz":float(Cz),


    }
def Charged_ring(q, px,py,pz , n=8, span=2):
    q=q*1e-9
    x1d = np.linspace(-span, span, n)
    y1d = np.linspace(-span, span, n)
    z1d = np.linspace(-span, span, n)
    X, Y, Z = np.meshgrid(x1d, y1d, z1d)
    R=10

    N=36
    theta=np.linspace(0, 2*np.pi, N,endpoint=False)
    xi=R*np.cos(theta)
    yi=R*np.sin(theta)
    zi=np.zeros(N)
    qi=(q*1e-9)/N

    pEx=pEy=pEz=0
    for i in range(N):
        rx=px-xi[i]
        ry=py-yi[i]
        rz=pz-zi[i]
        r=np.sqrt(rx**2+ry**2+rz**2)
    if r<1e-9:
        return{"ok":False,"message":"Probe is on Ring"}
    pEx +=k*qi*rx/r**3
    pEy +=k*qi*ry/r**3
    pEz +=k*qi*rz/r**3



    rx=X-0
    ry=Y-0
    rz=Z-0


    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    r_safe = np.maximum(r, 1e-9)
    Ex = K * q * rx / r_safe ** 3
    Ey = K * q * ry / r_safe ** 3
    Ez = K * q * rz / r_safe ** 3
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


def Relative_permittivity(q, x, y, z, px, py, pz,m, n=8, span=100):
    q = q * 1e-9
    x1d = np.linspace(-span, span, n)
    y1d = np.linspace(-span, span, n)
    z1d = np.linspace(-span, span, n)
    X, Y, Z = np.meshgrid(x1d, y1d, z1d)
    rx = X - x
    ry = Y - y
    rz = Z - z
    r = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2)
    r_safe = np.maximum(r, 1e-9)
    r_min=12

    k=K/m
    Ex = k * q * rx / r_safe ** 3
    Ey = k * q * ry / r_safe ** 3
    Ez = k * q * rz / r_safe ** 3

    prx = px - x
    pry = py - y
    prz = pz - z

    pr = np.sqrt(prx ** 2 + pry ** 2 + prz ** 2)
    pV = k * q / pr

    if pr < 1e-9:
        return {"ok": False, "message": "Your probe is at the charge point itself"}

    pEx = k * q * prx / pr ** 3
    pEy = k * q * pry / pr ** 3
    pEz = k * q * prz / pr ** 3

    Emag = np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)
    if Emag.max() == 0:
        return {"ok": False, "message": "Electric Field is zero"}

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
        "Ex": float(pEx),
        "Ey": float(pEy),
        "Ez": float(pEz),
        "Emag": float(PEmag),
        "qx": float(x),
        "qy": float(y),
        "qz": float(z),
        "px": float(px),
        "py": float(py),
        "pz": float(pz),
        "c": c_vals.tolist(),
        "cmin": float(np.percentile(c_vals, 5)),
        "cmax": float(np.percentile(c_vals, 95)),
        "V": float(pV),
        "m":float(m),

    }
