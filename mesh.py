from point import Point
from segment import Segment
from triangle import Triangle

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

    def GmshToMesh(self):

        # Création des points
        coordonnees = gmsh.model.mesh.getNodes()[1]
        X = coordonnees[0:-1:3]
        Y = coordonnees[1:-1:3]

        self.Npts = len(gmsh.model.mesh.getNodes()[0])
        for pts in range(self.Npts):
            point = Point(X[pts], Y[pts])
            self.points.append(point)

        # Création des éléments
        PhysicalGroups = gmsh.model.getPhysicalGroups()

        for dim, physical_tag in PhysicalGroups:
            entities = gmsh.model.getEntitiesForPhysicalGroup(dim, physical_tag)
            for entity in entities:
                # Ajouter des segments
                if dim == 1:
                    segments = gmsh.model.mesh.getElements(dim, entity)[2][0]
                    x = segments[0::2]
                    y = segments[1::2]
                    
                    for i in range(len(x)):
                        points = []
                        points.append(self.points[int(x[i]-1)])
                        points.append(self.points[int(y[i]-1)])
                        segment = Segment(points, physical_tag)
                        self.segments.append(segment)
                        self.Nseg += 1

                if dim == 2:
                    triangles = gmsh.model.mesh.getElements(dim, entity)[2][0]
                    
                    x = triangles[0::3]
                    y = triangles[1::3]
                    z = triangles[2::3]
                    
                    for i in range(len(x)):
                        points = []
                        points.append(self.points[int(x[i]-1)])
                        points.append(self.points[int(y[i]-1)])
                        points.append(self.points[int(z[i]-1)])
                        triangle = Triangle(points, physical_tag)
                        self.triangles.append(triangle)
                        self.Ntri += 1


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
mesh.GmshToMesh()

# ==============
# Finalize GMSH
gmsh.finalize()
 
