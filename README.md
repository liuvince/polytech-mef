# Rendu / Projet 2019 - 2020

Vincent LIU, Karl MONGOSSO - MAIN 5 Polytech Sorbonne

## Code élément finis P1

* common.py contient les classes: Triplets, Point, Segment, Triangle

* geo.py contient la classe mesh, qui représente le maillage

* fem\_p1.py contient les classes: Mass, Stiffness, Integrale, Dirichlet

## Résolution du problème (1)

* Nous avons installé localement la bibliothèque GMSH SDK, comme indiqué sur : https://bthierry.pages.math.cnrs.fr/tutorial/gmsh/#local-in-the-folder-meh

* Modifier PATH\_TO\_GMSH\_LIB dans:

```
config.py
```

* Lancer le script:

```
python3 resolution.py
```

* Vous devez obtenir la solution dans:

```
output/usol.png
```

## Calcul de l'erreur en norme L2 entre la solution exacte et la solution approchée

* Modifier PATH\_TO\_GMSH\_LIB dans:

```
config.py
```

* Lancer le script:

```
python3 compute_error.py
```

* Vous devez obtenir la solution dans:

```
output/error.png
```

## Page du cours

* https://bthierry.pages.math.cnrs.fr/teaching/mefi\_main5/
