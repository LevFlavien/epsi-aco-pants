import math
import pants
import csv
import networkx as nx

manual = str(input("Paramétrage manuel (y/n) : ")) in ['y', 'Y']

if (manual):
    print("Saisissez les pamètres suivants (vide pour valeur par défaut) :")
    nbLines = int(input("Nombre de lignes à importer (-1 pour le fichier entier) : ") or 500)
    alpha = float(input("Importance des phéromones : ") or 1)
    beta = float(input("Importance de la distance : ") or 3)
    rho = float(input("Pourcentage d'évaporation des phéromones : ") or 0.8)
    q = float(input("Quantité max de phéromones par itération : ") or 1)
    t0 = float(input("Nivieau initial de phéromones : ") or 0.01)
    limit = int(input("Nombre d'itérations : ") or 100)
    ant_count = int(input("Nombre de fourmis : ") or 10)
    elite = float(input("Force des élites : ") or 0.5)
else :
    nbLines = 500

# Fonction de calcul de la distance entre deux nodes
def calcDistance(a, b):
    d = math.sqrt(math.pow((b[0] - a[0]), 2) + math.pow((b[1] - a[1]), 2))
    return d;

# Lecture du CSV et récupération des coordonnées
nodes = []
with open('open_pubs.csv', 'r') as csvfile:
    rows = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
    for row in rows:
        try:
            x = float(row[4])
            y = float(row[5])
            nodes.append((x, y))
        except:
            continue
        nbLines -= 1
        if nbLines == 0:
            break

# Retrait des doublons
nodes = set(nodes)
nodes = list(nodes)

# Génération de la solution
world = pants.world.World(nodes, calcDistance)

if (manual):
    solver = pants.solver.Solver(alpha=alpha, beta=beta, rho=rho, q=q, t0=t0, limit=limit, ant_count=ant_count, elite=elite)
else:
    solver = pants.solver.Solver()

solution = solver.solve(world)

print("Distance totale = ", solution.distance)

# Récupération de la distance parcourue entre chaque point et génération du graphique
graph = nx.Graph()
distances = []
for edge in solution.traveled:
    distances.append(edge.length)
    graph.add_edges_from([(edge.start, edge.end)])

nx.draw(graph)

print("Distance Moyenne entre chaque bar = " + str(sum(distances) / len(distances)))
