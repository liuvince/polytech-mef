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
                a = sqrt((self.p[0][0]-self.p[1][0])**2+(self.p[0][1]-self.p[1][1])**2)
                b = sqrt((self.p[1][0]-self.p[2][0])**2+(self.p[1][1]-self.p[2][1])**2)
                c = sqrt((self.p[2][0]-self.p[0][0])**2+(self.p[2][1]-self.p[0][1])**2)
                p = (a + b + c) / 2                      
                area = sqrt(p*(p-a)*(p-b)*(p-c))
                return area

        def jac(self):
            """ Calcul le jacobien du segment """
            return (2*self.area())
