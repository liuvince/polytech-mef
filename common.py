from math import sqrt

class Triplet:
    def __init__(self):
        self.data = ([], ([], []))

    def append(self, I, J, val):
        self.data[0].append(val)
        self.data[1][0].append(I)
        self.data[1][1].append(J)

class Point:
    name = "Point"
    N = 1
    def __init__(self, x, y):
        self.id = self.N
        self.x = float(x)
        self.y = float(y)
        
        Point.N += 1

class Segment:
	N = 1	
	name = "Segment"

	def __init__(self, p, physical_tag):
		self.id = self.N
		self.p = p
		self.physical_tag = physical_tag

		Segment.N += 1
	

	def area(self):
		"""" Calcul la taille du segment """
		area = 0
		area += sqrt((self.p[1].x-self.p[0].x)**2+(self.p[1].y-self.p[0].y)**2)
	
		return area 

	def jac(self):
		""" Calcul le jacobien du segment """
		return self.area()

	def gaussPoint(self,order=2):
        area = self.area()
        param = []
	    phys = []

        if order==1:
	        poids = [1]

	    elif order==2:
            poids = [area/6,4*area/6,area/6]

            for point in self.p:
                phys.append((point.x,point.y))

        phys.append(((self.p[0].x+self.p[1].x)/2,(self.p[0].y+self.p[1].y)/2))

	    return poids, param, phys

	def phiRef(self, param, i):
        if i==0:
            return 1-param[0]-param[1]
        elif i==1:
            return param[0]
        else:
            return param[1]

    def phiGeo(self,param,i):
        if i==0:
            return 1-param[0]-param[1]
        elif i==1:
            return param[0]
        else:
            return param[1]

class Triangle:
    N = 1
    name = "Triangle"

    def __init__(self, p, physical_tag):
            self.id = self.N
            self.p = p
            self.physical_tag = physical_tag
            Triangle.N += 1

    def area(self):
        """" Calcul l'air du triangle """
                
        area = 0
        a = sqrt((self.p[0].x-self.p[1].x)**2+(self.p[0].y-self.p[1].y)**2)
        b = sqrt((self.p[1].x-self.p[2].x)**2+(self.p[1].y-self.p[2].y)**2)
        c = sqrt((self.p[2].x-self.p[0].x)**2+(self.p[2].y-self.p[0].y)**2)
        p = (a + b + c) / 2                      
        area = sqrt(p*(p-a)*(p-b)*(p-c))
        return area

    def jac(self):
        """ Calcul le jacobien du segment """
        return (2*self.area())

    def gaussPoint(self,order=2):
        if order==1:
            param = [(1/3,1/3)]       
        elif order==2:
            param = [(1/6,1/6),(4/6,1/6),(1/6,4/6)]

        poids = [1/6 for i in range(len(param))]

        phys = []
        for i in param:
            coord = (0,0)
            for j in range(3):
                coord[0] += phiGeo(i,j)*self.p[j].x
                coord[1] += phiGeo(i,j)*self.p[j].y

            phys.append(coord)


        return poids, param, phys


    def phiRef(self, param, i):
        if i==0:
            return 1-param[0]-param[1]
        elif i==1:
            return param[0]
        else:
            return param[1]

    def phiGeo(self,param,i):
        if i==0:
            return 1-param[0]-param[1]
        elif i==1:
            return param[0]
        else:
            return param[1]

		

