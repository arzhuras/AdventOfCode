from tools import *
from collections import deque


def showGraph(graph: dict) -> None:
    # print(graph)
    for key in sorted(graph):
        print(key, "->")
        for key2 in sorted(graph[key]):
            print(" ", key2, graph[key][key2])


def dijkstraAlgo(graph: dict, vertex: str) -> list:
    """
    Diskstra : recherche du plus court chemin depuis un noeud vers tous les noeuds accessibles
               dans un graphe pondéré
               renvoi pour chaque noeud la distance minimale
    """
    queue = deque([vertex])
    distance = {vertex: 0}
    while queue:
        print(str(queue))
        t = queue.popleft()
        # print("Visite du sommet " + str(t))
        for voisin in graph[t]:
            nouvelle_distance = distance[t] + graph[t][voisin]
            if voisin not in distance or nouvelle_distance < distance[voisin]:
                distance[voisin] = nouvelle_distance
                # print("  Met à jour le sommet " + str(voisin) + " avec la distance : " + str(nouvelle_distance))
                queue.append(voisin)

    # remove the node itself from the list
    del distance[vertex]

    return distance


def dijkstraAlgoWithPath(graph: dict, vertex: str) -> list:
    """
    Dijkstra : recherche du plus court chemin depuis un noeud vers tous les noeuds accessibles
               dans un graphe pondéré
               renvoi pour chaque noeud la distance minimale + le chemin depuis la source
    """
    queue = deque([vertex])
    distance = {vertex: (0, [vertex])}
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
    del distance[vertex]

    return distance


if __name__ == "__main__":
    init_script()

    # Liste d'ajacence du graphe
    # graph = {"A": {"B": 135, "C": 4}, "B": {"E": 5}, "C": {"E": 161, "D": 2}, "D": {"E": 3}, "E": {}}
    graph = {"A": {"B": 135, "C": 4}, "B": {"E": 5}, "C": {
        "E": 161, "D": 2}, "D": {"E": 3}, "E": {"D": 2}}
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
