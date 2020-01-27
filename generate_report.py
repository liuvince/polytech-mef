html = """
<!DOCTYPE html>
<html>
<body>

<h2>2019 - 2020 : Projet / Rendu</h2>

<p>
Vincent Liu - Karl Mongosso | MAIN 5
</p>

<p>
<strong>Problème de référence</strong>
</p>

<center><img src="data/edp.png"></center><br><br>

Nous prenons le carré unitaire <img src="data/omega.png"> et 
<img src="data/f.png"> de sorte que la solution exacte est connue et vaut<br><center> <img src="data/u.png"></center><br>

<p>
<strong>Solution approchée (éléments finis P1) </strong>
</p><br>
<center><img src="data/uref.png"></center><br>

<p>
<strong>Solution exacte connue</strong>
</p><br>
<center><img src="data/uref.png"></center><br>


<p>
<strong>Analyse de l'erreur </strong>
</p><br>
On calcule l'erreur en norme <img src="data/L2.png"> entre la solution exacte et la solution approchée pour le problème de référence. <br>
Voici la courbe de l'erreur en fonction de h en échelle log-log. <br>
<center><img src="data/uref.png"><br></center>

On calcule ensuite la pente de la courbe: <br><br>

<center> pente = 0.2 </center><br><br>

On en déduit la vitesse de convergence par rapport au pas de maillage h: <br><br>

<center> pente = 0.2 </center><br><br>
"""


html += """<strong>Tableaux des valeurs des erreurs </strong>
<table><tr><th>h</th><th>Erreur</th></tr>"""
 
for num in range(33,48):
 symb = chr(num)
 html += "<tr><td>"+str(symb)+ "</td><td>"+str(num)+"</td></tr>"

html += """<br><br></body>
</html>
"""

with open("output/RapportTest.html", 'w') as f:
	f.write(html)



