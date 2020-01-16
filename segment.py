class Segment:
	N = 0	
	name = "Segment"

	def __init__(self,Point[]):
		self.id = N
		self.p = Point[]
		self.physical_tag = -1 #???

		N += 1
	

	def area(self):
		"""" Calcul la taille du segment """
		area = 0
		for i in range(1,len(self.p)):
			area += sqrt((self.p[i][0]-self.p[i-1][0])^2+(self.p[i][1]-self.p[i-1][1])^2)
	
		return area 

	def jac(self):
		""" Calcul le jacobien du segment """
		return self.area()
		
