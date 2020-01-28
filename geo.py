from common import Point, Segment, Triangle
from math import sqrt

class Mesh:
    """ Classe qui représente le maillage et permettra d'effectuer des recherches d'éléments. """

    def __init__(self):
        self.points = [] 
        self.segments = []
        self.triangles = []
        self.Npts = 0
        self.Nseg = 0
        self.Ntri = 0

    def GmshToMesh(self, gmsh):
        """ Conversion des données issues de GMSH dans la stucture de données. """

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

                        # Recuperation des points
                        points.append(self.points[int(x[i]-1)])
                        points.append(self.points[int(y[i]-1)])

                        # Création du segment
                        segment = Segment(points, physical_tag)

                        # Calcul de l'aire
                        segment.area = area(segment)

                        # Ajout à la stucture de données
                        self.segments.append(segment)
                        self.Nseg += 1

                # Ajouter des triangles
                if dim == 2:
                    triangles = gmsh.model.mesh.getElements(dim, entity)[2][0]
                    x = triangles[0::3]
                    y = triangles[1::3]
                    z = triangles[2::3]
                    
                    for i in range(len(x)):
                        points = []

                        # Récupération des points
                        points.append(self.points[int(x[i]-1)])
                        points.append(self.points[int(y[i]-1)])
                        points.append(self.points[int(z[i]-1)])

                        # Création du triangle
                        triangle = Triangle(points, physical_tag)

                        # Calcul de l'aire
                        triangle.area = area(triangle)

                        # Ajout à la stucture de données
                        self.triangles.append(triangle)
                        self.Ntri += 1


    def getElements(self, dim, physical_tag):
        """ Retourne une liste de tous les éléments ayant la dimension dim et le tag physique physical_tag. """

        if dim == 1:
            elements = self.segments
        elif dim == 2:
            elements = self.triangles

        return [element for element in elements if element.physical_tag == physical_tag]

    def getPoints(self, dim, physical_tag):
        """ Retourne uniquement les points du domaine de dimension dim et de label physique physique physical_tag. """
    
        # Utilisation d'un ensemble pour éviter les doublons de Points
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

def area(element):
    """" Calcul l'aire de l'élément. """

    # Aire d'un segment
    if element.name == "Segment":
        area = sqrt((element.p[1].x-element.p[0].x)**2+(element.p[1].y-element.p[0].y)**2)

    # Aire d'un triangle
    if element.name == "Triangle":
        a = sqrt((element.p[0].x-element.p[1].x)**2+(element.p[0].y-element.p[1].y)**2)
        b = sqrt((element.p[1].x-element.p[2].x)**2+(element.p[1].y-element.p[2].y)**2)
        c = sqrt((element.p[2].x-element.p[0].x)**2+(element.p[2].y-element.p[0].y)**2)
        p = (a + b + c) / 2
        area = sqrt(p*(p-a)*(p-b)*(p-c))
    return area


