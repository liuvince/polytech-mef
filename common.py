from math import sqrt

class Triplet:
    """ Triplets de type (I, J, valeur) pour concaténer la matrice. """

    def __init__(self):
        self.data = ([], ([], []))

    def append(self, I, J, val):
        """ Ajoute le triplet [I, J, val] dans self. data. """

        self.data[0].append(val)
        self.data[1][0].append(I)
        self.data[1][1].append(J)

class Point:
    """ Element de type point: coordonnées et identifiant. """

    name = "Point"
    N = 1

    def __init__(self, x, y):
        self.id = self.N
        self.x = float(x)
        self.y = float(y)
        
        Point.N += 1

class Segment:
    """ Element de type segment: 2 Points, un identifiant et un tag physique. """

    N = 1	
    name = "Segment"

    def __init__(self, p, physical_tag):
        self.id = self.N
        self.p = p
        self.physical_tag = physical_tag
        self.area = 0 # On calcul, et on stock l'aire pour éviter de le recalculer
        
        Segment.N += 1

    def jac(self):
        """ Calcul le jacobien du segment. """

        return self.area
    
    def gaussPoint(self, order=2):
        """ Retourne les poids, les coordonnées paramétriques et les coordonnées physiques des points de Gauss de l'élément considéré, pour une précision order. """

        area = self.area()
        param = []
        phys = []
        if order==1:
            poids = [1]
        elif order==2:
            poids = [area/6,4*area/6,area/6]
            for point in self.p:    # s1 et s2
                phys.append((point.x,point.y))

        # Milieu s12
        phys.append(((self.p[0].x+self.p[1].x)/2,(self.p[0].y+self.p[1].y)/2))
        return poids, param, phys
    
    def phiRef(self, param, i):
        """ Fonctions d'interpolation de la solution. """

        if i==0:
            return 1-param[0]-param[1]
        elif i==1:
            return param[0]
        else:
            return param[1]

    def phiGeo(self, param, i):
        """ Fonction d'interpolation géométrique. """

        if i==0:
            return 1-param[0]-param[1]
        elif i==1:
            return param[0]
        else:
            return param[1]

class Triangle:
    """ Element de type triangle: 3 Points, un identifiant et un tag physique. """
    N = 1
    name = "Triangle"

    def __init__(self, p, physical_tag):
            self.id = self.N
            self.p = p
            self.physical_tag = physical_tag
            self.area = 0 # On calcule et on stock l'aire pour éviter de le recalculer
            Triangle.N += 1

    def jac(self):
        """ Calcul le jacobien du segment. """

        return 2*self.area

    def gaussPoint(self,order=2):
        """ Retourne les poids, les coordonnées paramétriques et les coordonnées physiques des points de Gauss de l'élément considéré, pour une précision order. """

        if order==1:
            param = [(1/3,1/3)]       
        elif order==2:
            param = [(1/6,1/6),(4/6,1/6),(1/6,4/6)]

        poids = [1/6 for i in range(len(param))]

        phys = []
        for i in param:
            coord = [0,0]
            for j in range(3):
                coord[0] += self.phiGeo(i,j)*self.p[j].x
                coord[1] += self.phiGeo(i,j)*self.p[j].y

            phys.append(tuple(coord))


        return poids, param, phys

    def phiRef(self, param, i):
        """ Fonctions d'interpolation de la solution. """

        if i==0:
            return 1-param[0]-param[1]
        elif i==1:
            return param[0]
        else:
            return param[1]

    def phiGeo(self,param,i):
        """ Fonction d'interpolation géométrique. """

        if i==0:
            return 1-param[0]-param[1]
        elif i==1:
            return param[0]
        else:
            return param[1]
