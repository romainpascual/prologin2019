import math

def marche_nocturne(n, liste_prix, b):
    """
    :param n: nombre de minerai rare
    :type n: int
    :param liste_prix: liste des prix de chaque minerai
    :type liste_prix: list[int]
    :param b: le total d'argent que vous souhaitez dépenser dans ce souvenir
    :type b: int
    """
    bestS = math.inf
    for i in range(n):
        s = 0
        for j in range(i,n):
            s += liste_prix[j]
            if s == b :
                bestS = min(bestS, j-i+1)
                break
            elif s > b:
                break
    if bestS == math.inf :
        print(-1)
    else :
        print(bestS)


if __name__ == '__main__':
    n = int(input())
    liste_prix = list(map(int, input().split()))
    b = int(input())
    marche_nocturne(n, liste_prix, b)