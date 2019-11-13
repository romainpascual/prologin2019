import numpy, collections, math

from profile import profile
from time import sleep

def buildDicts(l, h, n, flotte):
    """
    :param l: la largeur de la zone
    :type l: int
    :param h: la hauteur de la zone
    :type h: int
    :param n: Le nombre de vaisseaux dans la flotte
    :type n: int
    :param flotte: une liste de vaisseaux
    :type flotte: list[dict["x": int, "y": int, "u": int, "v": int]]

    Construit des dictionnaires qui stockent selon 
    x et y les cases occupées
    """
    # dict_x stocke pour chaque x la liste des vaisseaux 
    # (selon y de depart et la longueur)
    dict_x = {}

    # dict_y stocke pour chaque y la liste des vaisseaux 
    # (selon x de depart et la longueur)
    dict_y = {}

    # parcours des vaisseaux
    for f in flotte:
        x,y,u,v = f["x"], f["y"], f["u"], f["v"]

        # parcours des vaisseaux selon x
        for i in range(x,u):
            if i not in dict_x:
                dict_x[i] = [[y,v-y]]
            else :
                dict_x[i].append([y,v-y])

        # parcours des vaisseaux selon y
        for j in range(y,v):
            if j not in dict_y:
                dict_y[j] = [[x,u-x]]
            else :
                dict_y[j].append([x,u-x])

    return dict_x, dict_y

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

def processLigne(x, list_x, sommets, cases):
    """
    : param x : position en x de la liste concernee
    : type x : int
    : param list_x : cases occupees sur la ligne x
    : type x : list[int,int]
    """
    # suppression des collisions
    suppressionCollision(list_x)

    # ajout des sommets
    for cases_adj in list_x :

        # recuperation des valeurs
        y_deb = cases_adj[0]
        t = cases_adj[1]

        # ajout du sommet
        #sommets.append({"x":x, "y":y_deb, "o":"x", "t":t})
        sommets.append(len(sommets))

        # mise a jour des cases
        for y in range(y_deb, y_deb+t):
            cases[x,y] = [len(sommets)-1]

def processColonne(y, list_y, sommets, cases):
    """
    : param y : position en y de la liste concernee
    : type y : int
    : param list_y : cases occupees sur la ligne y
    : type y : list[int,int]
    """
    # suppression des collisions
    suppressionCollision(list_y)

    # ajout des sommets
    for cases_adj in list_y :

        # recuperation des valeurs
        x_deb = cases_adj[0]
        t = cases_adj[1]

        # ajout du sommet
        #sommets.append({"x":x_deb, "y":y, "o":"y", "t":t})
        sommets.append(len(sommets))

        # mise a jour des cases
        for x in range(x_deb, x_deb+t):
            cases[x,y].append(len(sommets)-1)


def buildGraphe(dict_x, dict_y):
    """
    : param dict_x: cases occupées par x
    : type dict_x: dict{key:int, value:list[int,int]}
    : param dict_y: cases occupées par y
    : type dict_y: dict{key:int, value:list[int,int]}

    Construit le graphe bipartite :
    Chaque segment maximal composé de cases adjacentes de flotte,
    correspond à un emplacement potentiel de laser et génère un 
    sommet.

    Les aretes sont orientées des sommets x vers les sommets y
    """
    sommetsX = []
    sommetsY = []
    aretesX = {}
    cases = {}

    # process x
    for x in dict_x.keys():
        processLigne(x, dict_x[x], sommetsX, cases)

    # process y
    for y in dict_y.keys():
        processColonne(y, dict_y[y], sommetsY, cases)


    for case in cases.values():
        x, y = case[0], case[1]
        if x not in aretesX :
            aretesX[x] = [y]
        else :
            aretesX[x].append(y)

    del(cases)

    return sommetsX, sommetsY, aretesX

@profile
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

    dict_x, dict_y = buildDicts(l,h,n,flotte)

    sommetsX, sommetsY, aretesX = buildGraphe(dict_x, dict_y)
    del(dict_x)
    del(dict_y)

    return(HopcroftKarp(sommetsX, sommetsY, aretesX))

def HopcroftKarp(sommetsX, sommetsY, aretesX):
    """
    https://fr.wikipedia.org/wiki/Algorithme_de_Hopcroft-Karp
    """
    pair_X = {}
    pair_Y = {}
    dist = {}
    for x in sommetsX:
        pair_X[x] = 'nil'
    for y in sommetsX:
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

if __name__ == '__main__':
    l = int(input())
    h = int(input())
    n = int(input())
    flotte = [
        dict(zip(("x", "y", "u", "v"), map(int, input().split())))
        for _ in range(n)
        ]

    runInput = 1
    if runInput:
        print(forcecontreflotte(l, h, n, flotte))
    
    # test suppressionCollision
    testSuppressionCollision = 0
    if testSuppressionCollision:
        l = [[1,2], [0,5], [0,2], [6,1], [7,1], [8,1], [1,1], [3,1], [8,2], [1,3]]
        suppressionCollision(l)
        print(l == [[0, 5], [6, 4]])

        # ok

    # test jedi 1
    l, h, n = 5, 5, 2
    flotte = [dict(zip(("x", "y", "u", "v"), (0,2,2,4))), \
              dict(zip(("x", "y", "u", "v"), (3,2,4,3))),  ]

    # test jedi 2
    l, h, n = 5, 5, 3
    flotte = [dict(zip(("x", "y", "u", "v"), (3,2,4,3))), \
              dict(zip(("x", "y", "u", "v"), (1,3,5,4))), \
              dict(zip(("x", "y", "u", "v"), (3,4,4,5))),  ]


    # test buildDicts
    testBuildDicts = 0
    if testBuildDicts:
        dict_x, dict_y = buildDicts(l,h,n,flotte)
        print(dict_x)
        print(dict_y)

        #  ok

    # test sommetsX
    testSommetsX = 0
    if testSommetsX:
        dict_x, dict_y = buildDicts(l,h,n,flotte)

        sommetsX = []
        cases = {}
        # process x
        for x in dict_x.keys():
            processLigne(x, dict_x[x], sommetsX, cases)

        print(sommetsX)
        print(cases)

        # ok

    # test sommetsY
    testSommetsY = 0
    if testSommetsY:
        dict_x, dict_y = buildDicts(l,h,n,flotte)

        sommetsX = []
        cases = {}

        # process x
        for x in dict_x.keys():
            processLigne(x, dict_x[x], sommetsX, cases)

        sommetsY = []
        # process y
        for y in dict_y.keys():
            processColonne(y, dict_y[y], sommetsY, cases)

        print(sommetsX)
        print(sommetsY)
        print(cases)

        # ok

    # test buildGraphe
    testBuildGraphe = 0
    if testBuildGraphe:
        dict_x, dict_y = buildDicts(l,h,n,flotte)
        sommetsX, sommetsY, aretesX = buildGraphe(dict_x, dict_y)
        print(sommetsX)
        print(sommetsY)
        print(aretesX)

    # test forcecontreflotte
    testForcecontreflotte = 0
    if testForcecontreflotte:
        res = forcecontreflotte(l,h,h,flotte)
        print(res)