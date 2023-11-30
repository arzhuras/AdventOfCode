class Data:
    rawInput = []
    line = []
    valves = {}


data = Data()


class Valve:
    pass


print(data.rawInput)


class Point:
    "Definition d'un point geometrique"
    toto = "toto"


a = Point()
a.x = 1
a.y = 2
a.tata = "tata"
b = Point()
b.x = 3
b.y = 4
b.tata = "tatab"
print("a : x =", a.x, "y =", a.y, a.toto, a.tata)
print("b : x =", b.x, "y =", b.y, b.toto, b.tata)


b = a
print("a : x =", a.x, "y =", a.y)
print("b : x =", b.x, "y =", b.y)
a.x = 3
a.y = 4
print("a : x =", a.x, "y =", a.y)
print("b : x =", b.x, "y =", b.y)