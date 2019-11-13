
def interferences(n, s):
    """
    :param n: la longueur du message
    :type n: int
    :param s: le message
    :type s: str
    """
    msg = ""
    read = True
    for c in s:
        if c =='*':
            read = not read
        elif c == '.' :
            pass
        elif read :
            msg += c
    print(msg)


if __name__ == '__main__':
    n = int(input())
    s = input()
    interferences(n, s)
