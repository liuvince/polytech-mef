import sys
import os
from config import PATH_TO_GMSH_LIB
sys.path.insert(0, PATH_TO_GMSH_LIB)


import gmsh
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from numpy.linalg import norm
import geo
import fem_p1
import common

#Données
def g(x,y):
   return np.sin(np.pi*x)*np.sin(np.pi*y)
def f(x,y):
    return g(x,y)*(2*np.pi*np.pi +1)
def diri(x,y):
    return 0

if __name__ == "__main__":
    
    OUT_DIRECTORY = "output"
    output_u = os.path.join(OUT_DIRECTORY, "usol.png")
    output_uref = os.path.join(OUT_DIRECTORY, "uref.png")

    if not os.path.exists(OUT_DIRECTORY):
        os.mkdir(OUT_DIRECTORY)

    # Parameter
    h = 0.1

    # ==============
    gmsh.initialize(sys.argv)
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", h);
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", h);

    # Model
    model = gmsh.model
    model.add("Square")
    # Rectangle of (elementary) tag 1
    factory = model.occ
    factory.addRectangle(0, 0, 0, 1, 1, 1)
    # Sync
    factory.synchronize()
    # Physical groups
    gmsh.model.addPhysicalGroup(1, [1, 2, 3, 4], 1)
    gmsh.model.addPhysicalGroup(2, [1], 10)
    # Mesh (2D)
    model.mesh.generate(2)

    # ==============
    # Maillage
    mesh = geo.Mesh()
    mesh.GmshToMesh(gmsh)

    # Triplets
    t = common.Triplet()
    print("[resolution.py] Calcul Matrice de Masse ...")
    fem_p1.Mass(mesh, 2, 10, t)
    print("[resolution.py] Calcul Matrice de Rigidité ...")
    fem_p1.Stiffness(mesh, 2, 10, t)

    b = np.zeros((mesh.Npts,)) 
    print("[resolution.py] Calcul du second membre ...")
    fem_p1.Integrale(mesh, 2, 10, f, b, 2)
    print("[resolution.py] Prise en compte de la condition de Dirichlet ...")
    fem_p1.Dirichlet(mesh, 1, 1, diri, t, b)

    # Résolution
    A = coo_matrix(t.data).tocsr()
    print("[resolution.py] Résolution du système linéaire ...")
    U = spsolve(A, b)
    # Visualisation

    x= [pt.x for pt in mesh.points]
    y= [pt.y for pt in mesh.points]
       
    ### U approché
    connectivity=[]
    for tri in mesh.triangles:
        connectivity.append([p.id - 1 for p in tri.p]) 

    plt.clf()
    plt.tricontourf(x, y, connectivity, U, 12)
    plt.colorbar()
    plt.title("U approché pour h = {}".format(h))
    plt.savefig(output_u)
    plt.show()

    print("[resolution.py] figure sauvegardée sur : {}".format(output_u))

    ### U de référence
    Uref = np.zeros((mesh.Npts,))
    for pt in mesh.points:
        I = int(pt.id - 1)
        Uref[I] = g(pt.x, pt.y)

    plt.tricontourf(x, y, connectivity, Uref, 12)
    plt.colorbar()
    plt.title("U ref pour h = {}".format(h))
    plt.savefig(output_uref)
    plt.show()

    print("[resolution.py] figure sauvegardée sur : {}".format(output_uref))

    print("[resolution.py] Erreur en norme L2: {}".format(fem_p1.Error(mesh, 2, 10, Uref, U, 2)))

    # ==============
    # Finalize GMSH
    gmsh.finalize()
