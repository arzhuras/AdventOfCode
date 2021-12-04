import sys, os
import timeit
import re 

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} - {INPUT_FILE_NAME}===")

def customs():
    groupCount = 0
    groupSum = 0
    allGroupSum = 0
    groupDict = {}
    with open(INPUT_FILE_NAME, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            if (len(line) == 0) :
                groupCount = groupCount + 1
                groupSum = sum(groupDict.values())
                allGroupSum += groupSum
                print(f"[{groupCount}] sum:{groupSum} {groupDict} ")
                groupDict = {}
                #print()
                continue

            #print(">",line)
            for i in range(len(line)):
                groupDict[line[i]] = int(1)
    return allGroupSum

def customs2():
    groupCount = 0
    personCount = 0
    groupSum = 0
    allGroupSum = 0
    groupDict = {}
    with open(INPUT_FILE_NAME, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            if (len(line) == 0) :
                groupCount = groupCount + 1
                groupSum = 0
                for val in groupDict.values():
                    #print(personCount, groupDict, key, val)
                    if (val == personCount) :
                        groupSum += 1
                allGroupSum = allGroupSum + groupSum
                print(f"[{groupCount}] person:{personCount} common_answer:{groupSum} {groupDict} ", file=sys.stderr)
                groupDict = {}
                personCount = 0
                #print()
                continue

            #print(">",line)
            personCount += 1
            for i in range(len(line)):
                if (line[i] in groupDict):
                    groupDict[line[i]] += int(1)
                else :
                    groupDict[line[i]] = int(1)
    return allGroupSum

###
### PART 1
###

print()
print(f"### PART 1 ###")

yesCount = customs()

print()
print(f"result part 1 = {yesCount}")

###
### PART 2
###

print()
print(f"### PART 2 ###")

yesCount = customs2()

print()
print(f"result part 2 = {yesCount}")