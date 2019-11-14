import collections, math

def suppressionCollision(l):
    """
    : param l : liste de debuts, longueurs
    : type l : list[int,int]

    Supression des collisions
    """
    # tri par y croissant
    l.sort(key=lambda case : case[0])

    i_curr = 0
    while i_curr < len(l) :

        # recupere les cases adjacentes courantes
        cases_adj = l[i_curr]
        debut, fin = cases_adj[0], cases_adj[0] + cases_adj[1]

        # suivant
        i_suivant = i_curr + 1

        # collision
        while i_suivant < len(l) and l[i_suivant][0] <= fin :
            suivant = l.pop(i_suivant)
            fin = max(fin, suivant[0] + suivant[1])
        
        # mise a jour
        l[i_curr] = [debut, fin-debut]
        i_curr += 1

def buildGraphe(l, h, n, flotte):
    """
    :param l: la largeur de la zone
    :type l: int
    :param h: la hauteur de la zone
    :type h: int
    :param n: Le nombre de vaisseaux dans la flotte
    :type n: int
    :param flotte: une liste de vaisseaux
    :type flotte: list[dict["x": int, "y": int, "u": int, "v": int]]

    Construit le graphe bipartite :
    Chaque segment maximal composé de cases adjacentes de flotte,
    correspond à un emplacement potentiel de laser et génère un 
    sommet.

    Les aretes sont orientées des sommets x vers les sommets y
    """

    ###
    # Construction des dictionnaires qui stockent selon 
    # x et y les cases occupées

    # dict_x stocke pour chaque x la liste des vaisseaux 
    # (selon y de depart et la longueur)
    # dict_y stocke pour chaque y la liste des vaisseaux 
    # (selon x de depart et la longueur)
    ###

    dict_x = {}
    dict_y = {}
    sommetsX = []
    sommetsY = []
    aretesX = {}
    case2vertex_x = {}

    for f in flotte:
        x,y,u,v = f["x"], f["y"], f["u"], f["v"]

        for i in range(x,u):
            if i not in dict_x:
                dict_x[i] = [[y,v-y]]
            else :
                dict_x[i].append([y,v-y])

        for j in range(y,v):
            if j not in dict_y:
                dict_y[j] = [[x,u-x]]
            else :
                dict_y[j].append([x,u-x])
    
    ###
    # Construction du graphe à partir des dictionnaires.
    ###

    # process x
    for x in dict_x.keys():
        suppressionCollision(dict_x[x])
        for cases_adj in dict_x[x] :

            # recuperation des valeurs
            y_deb = cases_adj[0]
            t = cases_adj[1]

            # ajout du sommet
            sommetsX.append(len(sommetsX))

            # mise a jour des cases
            for y in range(y_deb, y_deb+t):
                case2vertex_x[x,y] = len(sommetsX)-1

    # process y
    for y in dict_y.keys():
        suppressionCollision(dict_y[y])

        # ajout des sommets
        for cases_adj in dict_y[y] :

            # recuperation des valeurs
            x_deb = cases_adj[0]
            t = cases_adj[1]

            # ajout du sommet
            sommetsY.append(len(sommetsY))

            # mise a jour des cases
            for x in range(x_deb, x_deb+t):
                vertex_x = case2vertex_x[x,y]
                if vertex_x not in aretesX :
                    aretesX[vertex_x] = [len(sommetsY)-1]
                else :
                    aretesX[vertex_x].append(len(sommetsY)-1)

    ###
    # Liberation memoire
    ###
   
    del(dict_x)
    del(dict_y)
    del(case2vertex_x)

    return sommetsX, sommetsY, aretesX

###
# Algorithme de Hopcroft-Karp pour calculer Vertex Cover :
# pour un graphe bipartite, Vertex Cover = 
###


def HopcroftKarp(sommetsX, sommetsY, aretesX):
    """
    https://fr.wikipedia.org/wiki/Algorithme_de_Hopcroft-Karp
    """
    pair_X = {}
    pair_Y = {}
    dist = {}
    for x in sommetsX:
        pair_X[x] = 'nil'
    for y in sommetsY:
        pair_Y[y] = 'nil'
    
    matching = 0
    while BFS(sommetsX, aretesX, pair_X, pair_Y, dist):
        for x in sommetsX:
            if pair_X[x] == 'nil':
                if DFS(x, aretesX, pair_X, pair_Y, dist):
                    matching += 1
    
    return matching

def BFS(sommetsX, aretesX, pair_X, pair_Y, dist):
    queue = collections.deque()
    for x in sommetsX :
        if pair_X[x] == 'nil':
            dist[x] = 0
            queue.append(x)
        else:
            dist[x] = math.inf
    dist['nil'] = math.inf

    while queue:
        vertex_x = queue.popleft()
        if dist[vertex_x] < dist['nil']:
            for vertex_y in aretesX[vertex_x]:
                if dist[pair_Y[vertex_y]] == math.inf:
                    dist[pair_Y[vertex_y]] = dist[vertex_x] +1
                    queue.append(pair_Y[vertex_y])
    return dist['nil'] != math.inf

def DFS(vertex_x, aretesX, pair_X, pair_Y, dist):
    if vertex_x != 'nil':
        for vertex_y in aretesX[vertex_x]:
            if dist[pair_Y[vertex_y]] == dist[vertex_x] +1 :
                if DFS(pair_Y[vertex_y], aretesX, pair_X, pair_Y, dist):
                    pair_Y[vertex_y] = vertex_x
                    pair_X[vertex_x] = vertex_y
                    return True
        dist[vertex_x] = math.inf
        return False
    return True

def forcecontreflotte(l, h, n, flotte):
    """
    :param l: la largeur de la zone
    :type l: int
    :param h: la hauteur de la zone
    :type h: int
    :param n: Le nombre de vaisseaux dans la flotte
    :type n: int
    :param flotte: une liste de vaisseaux
    :type flotte: list[dict["x": int, "y": int, "u": int, "v": int]]
    """

    sommetsX, sommetsY, aretesX = buildGraphe(l,h,n,flotte)
    return(HopcroftKarp(sommetsX, sommetsY, aretesX))


if __name__ == '__main__':
    l = int(input())
    h = int(input())
    n = int(input())
    flotte = [
        dict(zip(("x", "y", "u", "v"), map(int, input().split())))
        for _ in range(n)
        ]
    print(forcecontreflotte(l, h, n, flotte))