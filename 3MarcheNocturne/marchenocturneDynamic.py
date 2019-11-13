import math

@profile
def marche_nocturne(n, liste_prix, b):
    """
    :param n: nombre de minerai rare
    :type n: int
    :param liste_prix: liste des prix de chaque minerai
    :type liste_prix: list[int]
    :param b: le total d'argent que vous souhaitez dépenser dans ce souvenir
    :type b: int
    """
    currS = 0
    currI = 0
    minSize = math.inf
    bestI, bestJ = -1, -1
    for j in range(n):
        if liste_prix[j] == 0:
            pass
        currS += liste_prix[j]
        if currS > b :
            while currS > b and currI <j :
                currS -= liste_prix[currI]
                currI += 1
        if currS == b :
            currSize = j - currI + 1
            if currSize < minSize :
                minSize, bestI, bestJ = currSize, currI, j
    if minSize ==  math.inf:
        print(-1)
    else :
        print(minSize)#, bestI, bestJ)

    # TODO Le nombre minimal de minerai que vous rapporterez, ou -1 si ce n'est
    # pas possible de résoudre le problème.
    pass


if __name__ == '__main__':
    n = int(input())
    liste_prix = list(map(int, input().split()))
    b = int(input())
    marche_nocturne(n, liste_prix, b)
