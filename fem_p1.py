import numpy as np

# element = Segment ou Triangle ; triplets = Triplets ; alpha un scalaire optionnel
def mass_elem(element, triplets):
    
    area = element.area()
    if element.name == "Triangle":
        M = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]]) / 12
    elif element.name == "Segment":
        M = np.array([[2, 1], [1, 2]]) / 6

    points = element.p

    for i, p1 in enumerate(points):
        I = p1.id - 1
        for j, p2 in enumerate(points):
            J = p2.id - 1
            triplets.append(I, J, M[i,j] * area)

# msh = Mesh, dim = int, physical_tag = int, triplets = Triplets
def Mass(msh, dim, physical_tag, triplets):

    elements = msh.getElements(dim, physical_tag)
    for element in elements:
        mass_elem(element, triplets)


def gradPhi(i):

    if i == 0:
        return np.array([[-1], [-1]])
    elif i == 1:
        return np.array([[1], [0]])
    elif i == 2:
        return np.array([[0], [1]])

def Bp(element):

    detJp = element.jac()

    output = np.zeros((2, 2))
    output[0, 0] = element.p[2].y - element.p[0].y
    output[0, 1] = element.p[0].y - element.p[1].y
    output[1, 0] = element.p[0].x - element.p[2].x
    output[1, 1] = element.p[1].x - element.p[0].x

    return output / detJp

def stiffness_elem(element, triplets):

    area = element.area()
    B = Bp(element)
    BB = B.T * B

    points = element.p
    for i, p1 in enumerate(points):
        gradPhi_i = gradPhi(i)
        I = p1.id - 1		# loc2glob
        for j, p2 in enumerate(points):
            gradPhi_j = gradPhi(j)
            J = p2.id - 1	# loc2glob
            val = area * (gradPhi_i.T.dot(BB)).dot(gradPhi_j)
            triplets.append(I, J, val[0,0])

# msh = Mesh, dim = int, physical_tag = int, triplets = Triplets  
def Stiffness(msh, dim, physical_tag, triplets):

    elements = msh.getElements(dim, physical_tag)
    for element in elements:
        stiffness_elem(element, triplets)

# msh: Mesh, dim: int, physical_tag:int, f, B:np.array, order=2
def Integrale(msh, dim, physical_tag, f, B, order=2):
    elements = msh.getElements(dim,physical_tag)

    for element in elements:
        poids, param, phys = element.gaussPoint(order)

        for i in range(3):
            I = element.p[i].id-1
            
            for m in range(len(param)):
                B[I] += poids[m]*f(phys[m][0],phys[m][1])*element.phiRef(param[m],i)


def Dirichlet(msh, dim, physical_tag, g, triplets, B):
    points = msh.getPoints(dim, physical_tag)
    ids = set([point.id for point in points])
    
    nPts = len(triplets.data[0])

    # Parcours des noeuds I du domaine de Dirichlet
    for i in range(nPts):
        I = triplets.data[1][0][i]
        # Si une occurence à I est obtenue, 
        # la valeur de ce triplet est mise à 0.
        if I + 1 in ids:
            triplets.data[0][i] = 0

    for point in points:
        I = point.id - 1
        x, y = point.x, point.y
        # Ajout d'un triplet (I, I, 1) correspondant au terme diagonal 
        triplets.append(I, I, 1)
        # Modifier le coefficient B[I] = g(x, y)
        B[I] = g(x, y)
 
