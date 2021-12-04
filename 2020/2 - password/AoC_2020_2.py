import sys, os
import timeit

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} ===")

###
### PART 1
###
valid = 0
with open(INPUT_FILE_NAME, "r") as inputFile:
    for line in inputFile:
        line = line.replace("-", " ")
        line = line.replace(":", "")
        #print(line, end='')
        tmp = line.split()
        min = int(tmp[0])
        max = int(tmp[1])
        car = tmp[2]
        pwd = tmp[3]
        #print(min, max, car, pwd)
        occ = pwd.count(car)
        if (occ >= min and occ <= max ) :
            #print("YES", min, max, car, pwd, occ)
            valid = valid + 1
        else :
            #print("NO", min, max, car, pwd, occ)
            continue

print(f"### PART 1: valid = {valid}")

###
### PART 2
###
valid = 0
with open(INPUT_FILE_NAME, "r") as inputFile:
    for line in inputFile:
        line = line.replace("-", " ")
        line = line.replace(":", "")
        #print(line, end='')
        tmp = line.split()
        min = int(tmp[0]) - 1
        max = int(tmp[1]) - 1
        car = tmp[2]
        pwd = tmp[3]
        #print(min, max, car, pwd)
        if ((pwd[min] == car and pwd[max] != car) or (pwd[min] != car and pwd[max] == car) ) :
            #print("YES", min, max, car, pwd)
            valid = valid + 1
        else :
            #print("NO", min, max, car, pwd)
            continue

print(f"### PART 2: valid = {valid}")
