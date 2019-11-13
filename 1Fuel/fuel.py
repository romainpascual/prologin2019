import sys

sys.stdin.readline()
print(sum([60 if int(x) <= 90 else 80 for x in sys.stdin.readline().split()]))