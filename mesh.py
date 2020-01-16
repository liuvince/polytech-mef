from point import Point

class Mesh:
    def __init__(self):
        self.points = [] 
        self.segments = []
        self.triangles = []
        self.Npts = 0
        self.Nseg = 0
        self.Ntri = 0

    def __str__(self):
        return (self.Npts, self.Nseg, self.Ntri)

    def GmshToMesh(self, model):

        # Création des points
        coordonnees = model.getNodes()[1]
        X = coordonnees[0:-1:3]
        Y = coordonnees[1:-1:3]

        self.Npts = len(model.getNodes()[0])
        for pts in range(self.Npts):
            point = Point(X[pts], Y[pts])
            self.points.append(point)

    def getElements(self, dim, physical_tag):
        if dim == 1:
            return [segment for segment in self.segments if segment.physical_tag == physical_tag]
        if dim == 2:
            return [triangle for triangle in self.triangles if triangle.physical_tag == physical_tag]

    def getPoints(self, dim, physical_tag):
        points = set()
        if dim == 1:
            for segment in self.segments:
                if segment.physical_tag == physical_tag:
                    for point in segment.p:
                        points.add(point)
        if dim == 2:
            for triangle in self.triangles:
                if triangle.physical_tag == physical_tag:
                    for point in triangle.p:
                        points.add(point)
        return points

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
mesh.GmshToMesh(gmsh.model.mesh)
print(mesh.points[0].x)
print(mesh.points[0].y)

# ==============
# Finalize GMSH
gmsh.finalize()
 
