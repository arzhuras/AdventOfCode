from tools import *
from collections import deque
from collections import namedtuple


"""
site web pour tracer des graphes: https://graphonline.ru/fr/
Utiliser Créer un graphique: edge list

bibliothèque python graphviz a tester

"""


def showGraph(graph: dict) -> None:
    # print(graph)
    for key in sorted(graph):
        print(key, "->")
        for key2 in sorted(graph[key]):
            print(" ", key2, graph[key][key2])


def buildGraphFromGrid(grid: list, wall="#", cost=1) -> dict:
    """
    buildGraphFromGrid : construit un graph a partir d'une grid avec un cout par défaut
    """
    offsetTuple = namedtuple("offset", ["y", "x"])
    # offset neihgbors (y,x)
    N = offsetTuple(-1, 0)
    W = offsetTuple(0, -1)
    E = offsetTuple(0, +1)
    S = offsetTuple(+1, 0)

    graph = {}
    width = len(grid)
    height = len(grid[0])
    for y in range(width):
        for x in range(height):
            if grid[y][x] == wall:
                continue
            graph[(y, x)] = {}  # coordonnées y, x du noeud
            for offset in (N, E, S, W):
                nodeY = y + offset.y
                if nodeY < 0 or nodeY == width:
                    continue
                nodeX = x + offset.x
                if nodeX < 0 or nodeX == height:
                    continue

                if grid[nodeY][nodeX] != wall:
                    graph[(y, x)][(nodeY, nodeX)] = cost
    return graph


def dijkstraAlgo(graph: dict, originNode: tuple) -> list:
    """
    Diskstra : recherche du plus court chemin depuis un noeud vers tous les noeuds accessibles
               dans un graphe pondéré
               renvoi pour chaque noeud la distance minimale
    """
    queue = deque([originNode])
    distance = {originNode: 0}
    while queue:
        # print(str(queue))
        t = queue.popleft()
        # print("Visite du sommet " + str(t))
        for voisin in graph[t]:
            nouvelle_distance = distance[t] + graph[t][voisin]
            if voisin not in distance or nouvelle_distance < distance[voisin]:
                distance[voisin] = nouvelle_distance
                # print("  Met à jour le sommet " + str(voisin) + " avec la distance : " + str(nouvelle_distance))
                queue.append(voisin)

    # remove the node itself from the list
    del distance[originNode]

    return distance


def dijkstraAlgoWithPath(graph: dict, originNode: tuple) -> list:
    """
    Dijkstra : recherche du plus court chemin depuis un noeud vers tous les noeuds accessibles
               dans un graphe pondéré
               renvoi pour chaque noeud la distance minimale + le chemin depuis la source
    """
    queue = deque([originNode])
    distance = {originNode: (0, [originNode])}
    while queue:
        t = queue.popleft()
        # print("Visite du sommet " + str(t) + " " + str(queue))
        for voisin in graph[t]:
            nouvelle_distance = distance[t][0] + graph[t][voisin]
            if voisin not in distance or nouvelle_distance < distance[voisin][0]:
                distance[voisin] = nouvelle_distance, distance[t][1] + [voisin]
                # print("Met à jour le sommet " + str(voisin) + " avec la distance : " + str(nouvelle_distance))
                queue.append(voisin)

    # remove the node itself from the list
    del distance[originNode]

    return distance


if __name__ == "__main__":
    init_script()

    # Liste d'ajacence du graphe
    # graph = {"A": {"B": 135, "C": 4}, "B": {"E": 5}, "C": {"E": 161, "D": 2}, "D": {"E": 3}, "E": {}}
    graph = {
        "A": {"B": 135, "C": 4},
        "B": {"E": 5},
        "C": {"E": 161, "D": 2},
        "D": {"E": 3},
        "E": {"D": 2},
    }
    showGraph(graph)
    print()

    # dijkstra
    print(Ansi.blue)
    help(dijkstraAlgo)
    print(Ansi.norm)
    shortestDistance = {}
    for key in graph:
        shortestDistance[key] = dijkstraAlgo(graph, key)
    print(Ansi.green, "+=+ shortest distance +=+", Ansi.norm)
    showGraph(shortestDistance)
    print()

    # dijkstra with path
    print(Ansi.blue)
    help(dijkstraAlgoWithPath)
    print(Ansi.norm)

    shortestDistanceWithPath = {}
    for key in graph:
        shortestDistanceWithPath[key] = dijkstraAlgoWithPath(graph, key)
    print(Ansi.green, "+=+ shortest distance with path +=+", Ansi.norm)
    showGraph(shortestDistanceWithPath)
    print()
