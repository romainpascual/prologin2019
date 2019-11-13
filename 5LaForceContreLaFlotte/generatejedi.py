import random
l = random.randint(1,1000000)
h = random.randint(1,1000000)
N = random.randint(1,10000)

s = 0
flotte = []

for f in range(N):
    if s > 10000:
        break
    x = random.randint(0,l-1)
    y = random.randint(0,h-1)
    u = random.randint(x+1,min(l-1,x+15))
    v = random.randint(y+1,min(h-1,y+15))
    s += (u-x+1) * (v-y+1)
    t = (x,y,u,v)
    flotte.append(t)
    

print(l)
print(h)
print(len(flotte))
for t in flotte :
    for i in t:
        print(i, end= ' ')
    print()