from common import Point, Segment, Triangle

class Mesh:
    def __init__(self):
        self.points = [] 
        self.segments = []
        self.triangles = []
        self.Npts = 0
        self.Nseg = 0
        self.Ntri = 0

    def GmshToMesh(self, gmsh):

        # Création des points
        coordonnees = gmsh.model.mesh.getNodes()[1]
        X = coordonnees[0::3]
        Y = coordonnees[1::3]

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
            elements = self.segments
        elif dim == 2:
            elements = self.triangles

        return [element for element in elements if element.physical_tag == physical_tag]

    def getPoints(self, dim, physical_tag):

        points = set()
        if dim == 1:
            elements = self.segments
        elif dim == 2:
            elements = self.triangles

        for element in elements:
            if element.physical_tag == physical_tag:
                for point in element.p:
                    points.add(point)
        return points
 
