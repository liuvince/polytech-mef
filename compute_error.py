import sys
import os
from config import PATH_TO_GMSH_LIB
sys.path.insert(0, PATH_TO_GMSH_LIB)

import gmsh
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
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
    output = os.path.join(OUT_DIRECTORY, "error.png")

    if not os.path.exists(OUT_DIRECTORY):
        os.mkdir(OUT_DIRECTORY)

    # Parameter
    errors = []
    H = [0.5, 0.1, 0.05, 0.01, 0.005]
    for h in H:
           
        print("[compute_error.py] Calcul de l'erreur pour h = {}".format(h))

        # ==============
        gmsh.initialize(sys.argv)
        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", h)
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", h)
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
        fem_p1.Mass(mesh, 2, 10, t)
        fem_p1.Stiffness(mesh, 2, 10, t)
        b = np.zeros((mesh.Npts,)) 
        fem_p1.Integrale(mesh, 2, 10, f, b, 2)
        fem_p1.Dirichlet(mesh, 1, 1, diri, t, b)
        # Résolution
        A = coo_matrix(t.data).tocsr()
        U = spsolve(A, b)

        x = [pt.x for pt in mesh.points]
        y = [pt.y for pt in mesh.points]
        ### U de référence
        Uref = np.zeros((mesh.Npts,))
        for pt in mesh.points:
            I = int(pt.id - 1)
            Uref[I] = g(pt.x, pt.y)
                
        # ==============
        # Finalize GMSH
        gmsh.finalize()
            
        # Reset
        common.Point.N = 1
        common.Segment.N = 1
        common.Triangle.N = 1

        # Calcul de l'erreur
        error = norm(U-Uref, 2)
        errors.append(error)
        print("[compute_error.py] h = {} | error = {}".format(h, error))

    # Visualisation
    plt.plot(H, errors, linestyle="--", marker='o', color='b')
    plt.xlabel("h")
    plt.ylabel("Erreur en norme L2")
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Erreur en fonction de h (échelle log-log)")
    plt.savefig(output)
    plt.show()
