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

	#def gaussPoint(self,order=2):
	#	poids = 1/6

	#	if order==1:
	#		param = (1/3,1/3)		
	#		
	#	elif order==2:
	#		param = (1/6,1/6)	

	#	phys 

	#	return poids, param, phys

		

	
	#def phiRef(sel, param, i):	

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
            poids = 1/6
            if order==1:
                param = (1/3,1/3)       
            elif order==2:
                param = (1/6,1/6)
            phys = (self.phi(param,1)*self.p[0].x+self.phi(param,2)*self.p[1].x+self.phi(param,3)*self.p[2].x, self.phi(param,1)*self.p[0].y+self.phi(param,2)*self.p[1].y+self.phi(param,3)*self.p[2].y)
            return poids, param, phys


        def phiRef(sel, param, i):
            if i==1:
                return 1-param[0]-param[1]
            elif i==2:
                return param[0]
            else:
                return param[1]


		

