class Point:
    name = "Point"
    N = 1
    def __init__(self, x, y):
        self.id = self.N
        self.x = float(x)
        self.y = float(y)
        
        self.N += 1
        
