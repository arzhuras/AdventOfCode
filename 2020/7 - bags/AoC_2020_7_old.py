import sys, os
import timeit
import re 

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} - {INPUT_FILE_NAME}===")

inputLines = []

def readInputFile(file):
    inputLines = []
    with open(file, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines

def bags():
    bagDict = {}
    possibleBag = []
    for line in inputLines:
        field = line.split()
        #print(field)
        curBag = field[0] + "_" + field[1]
        bagDict[curBag] = []
        for i in range(4, len(field), 4):
            if (field[i] == "no"):
                bagDict[curBag] = []
            else:    
                bagDict[curBag].append([int(field[i]), field[i+1] + "_" + field[i+2]])
        #print(curBag, bagDict[curBag])
    print()

    guessList = "shiny_gold"
    while(len(guessList) > 0):
        print(f"# guessList= {guessList}")
        nextGuessList = []
        for bag, content in bagDict.items():
            print(bag, content)
            for subBag in content:
                #print(subBag)
                if (subBag[1] in guessList):
                    if (bag not in possibleBag):
                        possibleBag.append(bag)
                        nextGuessList.append(bag)
                        print("!!! match", bag, nextGuessList)
        guessList = nextGuessList
        print()
    
    print(possibleBag)
    return len(possibleBag)

def bags2():
    bagDict = {}
    bagSumDict = {} # [0:nb_subnode, 1:total subnode_sum]

    # initialisation structure de données
    finalisedList = [] # 0:bag_name, 1:bag_weight
    nextFinalisedList = [] # 0:bag_name, 1:bag_weight
    for line in inputLines:
        field = line.split()
        #print(field)
        curBag = field[0] + "_" + field[1]
        bagDict[curBag] = []
        for i in range(4, len(field), 4):
            if (field[i] == "no"):
                bagDict[curBag] = []
                finalisedList.append([curBag, 1])
            else:    
                bagDict[curBag].append([int(field[i]), field[i+1] + "_" + field[i+2]])
        bagSumDict[curBag] = [len(bagDict[curBag]), 1]
        print(curBag, bagDict[curBag])
    print("finalisedList=", finalisedList)
    print("bagSumDict=",bagSumDict)
    print()

    # résolution
    while(len(finalisedList) > 0):
        print(f"# finalisedList= {finalisedList}")
        nextFinalisedList = []
        for bag, content in bagDict.items():
            for subBag in content:
                for finalName, finalWeight in finalisedList:
                    if (subBag[1] == finalName):
                        print()
                        print("bag=", bag, "content=", content)
                        print("subBag=", subBag)
                        print("finalName=", finalName, "finalWeight=", finalWeight)
                        print("bagSumDict[bag]=", bag, bagSumDict[bag])
                        bagSumDict[bag][0] -= 1
                        bagSumDict[bag][1] += subBag[0] * finalWeight
                        print("bagSumDict[bag]=", bag, bagSumDict[bag])
                        if (bagSumDict[bag][0] == 0): # on a finalisé un noeud
                            nextFinalisedList.append([bag, bagSumDict[bag][1]])
                            print("!!! nextFinalisedList=",nextFinalisedList)
                            if (bag == "shiny_gold") :
                                print("!!! FINISHED")
                                return bagSumDict[bag][1] - 1
        print("bagSumDict=",bagSumDict)
        print("nextFinalisedList=",nextFinalisedList)
        finalisedList = nextFinalisedList
        print()
    return -1

#inputLines = readInputFile("AoC_2020_7_sample.txt")
#inputLines = readInputFile("AoC_2020_7_sample2.txt")
inputLines = readInputFile(INPUT_FILE_NAME)
res = 0

###
### PART 1
###

print()
print(f"### PART 1 ###")

#res = bags()

print()
print(f"result part 1 = {res}")

###
### PART 2
###

print()
print(f"### PART 2 ###")

res = bags2()

print()
print(f"result part 2 = {res}")