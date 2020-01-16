class Triplet:
    def __init__(self):
        self.data = ([], ([], []))

    def __str__(self):
        return str(self.data)

    def append(self, I, J, val):
        self.data[0].append(val)
        self.data[1][0].append(I)
        self.data[1][1].append(J)
