import sys
from config import PATH_TO_GMSH_LIB
sys.path.insert(0, PATH_TO_GMSH_LIB)


import gmsh
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix
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
	#gmsh.model.addPhysicalGroup(1, [2,3,4], 2)
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
	#fem_p1.Integral(msh, 2, 10, f, b, 2)
	fem_p1.Dirichlet(mesh, 1, 1, diri, t, b)

	# Résolution
	A = coo_matrix(t.data, (mesh.Npts, mesh.Npts)).tocsr()
	# U = sparse.linalg.spsolve(A, b)

	# Visualisation
	"""
	x= [pt.x for pt in msh.points]
	y= [pt.y for pt in msh.points]
	connectivity=[]
	for tri in msh.triangles:
		connectivity.append([ p.id for p in tri.p]) 

	plt.tricontourf(x, y, connectivity, U, 12)
	plt.colorbar()
	plt.show()

	### U de référence
	Uref = np.zeros((msh.Npts,))
	for pt in msh.points:
		I = int(pt.id) - 1
		Uref[I] = g(pt.x, pt.y)
	plt.tricontourf(x, y, connectivity, Uref, 12)
	plt.colorbar()
	plt.show()
	"""

	# ==============
	# Finalize GMSH
	gmsh.finalize()
