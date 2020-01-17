from math import sqrt

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

		
