from triplet import Triplet
from point import Point
from segment import Segment
from triangle import Triangle
from mesh import Mesh

import numpy as np

# element = Segment ou Triangle ; triplets = Triplets ; alpha un scalaire optionnel
def mass_elem(element, triplets):
    
    area = element.area()
    if element.name == "Triangle":
        M = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]]) / 12
    elif element.name == "Segment":
        M = np.array([[2, 1], [1, 2]]) / 6

    points = element.p

    for i, p1 in enumerate(points):
        I = p1.id - 1
        for j, p2 in enumerate(points):
            J = p2.id - 1
            # print(I, J, M[i,j])
            triplets.append(I, J, M[i,j] * area)

# msh = Mesh, dim = int, physical_tag = int, triplets = Triplets
def Mass(msh, dim, physical_tag, triplets):

    elements = msh.getElements(dim, physical_tag)
    for element in elements:
        mass_elem(element, triplets)


def gradPhi(i):
    if i == 0:
        return np.array([[-1], [-1]])
    elif i == 1:
        return np.array([[1], [0]])
    elif i == 2:
        return np.array([[0], [1]])

def Bp(element):
    detJp = element.jac()
    output = np.zeros((2, 2))
    output[0, 0] = element.p[2].y - element.p[0].y
    output[0, 1] = element.p[0].y - element.p[1].y
    output[1, 0] = element.p[0].x - element.p[2].x
    output[1, 1] = element.p[1].x - element.p[0].x
    return output / detJp

def stiffness_elem(element, triplets):
    print("a1")
    area = element.area()
    B = Bp(element)
    BB = B.T * B
    print("b1")
    points = element.p
    for i, p1 in enumerate(points):
        gradPhi_i = gradPhi(i)
        I = p1.id - 1
        for j, p2 in enumerate(points):
            gradPhi_j = gradPhi(j)
            J = p2.id - 1
            val = area * (gradPhi_i.T.dot(BB)).dot(gradPhi_j)
            #print(I, J, val)
            triplets.append(I, J, val[0,0])
    print("c1")
  

def Stiffness(msh, dim, physical_tag, triplets):
    #print("Vincent")
    #print()
    elements = msh.getElements(dim, physical_tag)
   # print("ok")
    for element in elements:
        print(element.id)
        stiffness_elem(element, triplets)

from scipy.sparse import coo_matrix
import sys
sys.path.insert(0, '/home/v/gmsh-4.4.1-Linux64-sdk/lib')
import gmsh
import sys
gmsh.initialize(sys.argv)
gmsh.option.setNumber("General.Terminal", 1)
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1);
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.1);
# Model
model = gmsh.model
model.add("Square")
# Rectangle of (elementary) tag 1
factory = model.occ
factory.addRectangle(0,0,0, 1, 1, 1)
# Sync
factory.synchronize()
# Physical groups
gmsh.model.addPhysicalGroup(1, [1], 1)
gmsh.model.addPhysicalGroup(1, [2,3,4], 2)
gmsh.model.addPhysicalGroup(2, [1], 10)
# Mesh (2D)
model.mesh.generate(2)
# ==============
# Code to test mesh element access will be added here !
mesh = Mesh()
mesh.GmshToMesh(gmsh)
t = Triplet()

# Mass(mesh, 2, 10, t)
# A = coo_matrix(t.data, (mesh.Npts, mesh.Npts)).tocsr()
#U = np.ones((mesh.Npts)) 
# print((U.T * A).dot(U))
print("a")
Stiffness(mesh, 2, 10, t)
print("b")
K = coo_matrix(t.data, (mesh.Npts, mesh.Npts)).tocsr()
U = np.ones((mesh.Npts))
print(K.dot(U))


# ==============
# Finalize GMSH
gmsh.finalize()
 
