import sys, os
import time

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} ===")

inputLines = []

def readInputFile(file = INPUT_FILE_NAME):
    'read the input file'

    inputLines = []
    print(f"-> read {file}")
    with open(file, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines

class Bag:
    bag_d = {} # all bags list dictionary

    def __init__(self, name):
        self.name = name
        self.weight = 0   # child total weight. 0 = not calculated yet
        self.child_d = {} # child dictionary [name]=quantity
        Bag.bag_d[name] = self

    def __str__(self):
        tmp = f"{self.name:12}"
        # List the bag childs
        for name, quantity in self.child_d.items():
            tmp += f" {str(quantity):>2}:{name:12}"
        return tmp

    def addChild(self, childQuantity, childName):
        'add a bag child to and existing bag with its quantity'
        
        self.child_d[childName] = childQuantity

    def getWeight(self):
        'return the bag total weight'

        if (self.weight >0):
            return self.weight
        elif (len(self.child_d) == 0):
            self.weight = 1
        else:
            self.weight = 1
            for name, quantity in self.child_d.items():
                self.weight += Bag.bag_d[name].getWeight() * quantity
        #print(f"{self.weight}:{self.name}")
        return self.weight

    @staticmethod
    def getBag(name):
        return Bag.bag_d[name]

def initBags():
    for line in inputLines:
        field = line.split()
        #print(field)
        bag = Bag(field[0] + "_" + field[1])
        for i in range(4, len(field), 4):
            if (field[i] != "no"):
                bag.addChild(int(field[i]), field[i+1] + "_" + field[i+2])
        #print(bag)

###
### PART 2
###

print()
print(f"### PART 2 ###")

tic = time.perf_counter()

#inputLines = readInputFile("AoC_2020_7_sample.txt")
#inputLines = readInputFile("AoC_2020_7_sample2.txt")
inputLines = readInputFile()
initBags()
bag = Bag.getBag("shiny_gold")
res = bag.getWeight() - 1

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
