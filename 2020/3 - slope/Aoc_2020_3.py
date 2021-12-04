import sys, os
import timeit

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} ===")

def slope(arg_right, arg_down):
    treeCount = 0
    cur_right = 0
    lineLen = 0
    cur_down = 0
    with open(INPUT_FILE_NAME, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            if (lineLen == 0) :
                lineLen = len(line)
                #print(f"{cur_right:>2} {cur_down:>2} _ {line}")
                continue
            cur_down = cur_down + 1
            if (cur_down < arg_down):
                #print(f"{cur_right:>2} {cur_down:>2} _ {line}")
                continue
            else :
                cur_down = 0
            cur_right = (cur_right + arg_right) % lineLen
            if (line[cur_right] == "#") :
                treeCount = treeCount + 1

                string_list = list(line)
                string_list[cur_right] = "X"
                line = "".join(string_list)

                #print(f"{cur_right:>2} {cur_down:>2} # {line}")
            else :
                string_list = list(line)
                string_list[cur_right] = "O"
                line = "".join(string_list)

                #print(f"{cur_right:>2} {cur_down:>2} . {line}")
    print(f"- slope ({arg_right},{arg_down}) = {treeCount}")
    return treeCount

###
### PART 1
###

print()
print(f"### PART 1 ###")

treeCount = slope(3,1)

print()
print(f"result part 1 = {treeCount}")

###
### PART 2
###

print()
print(f"### PART 2 ###")

factorTreeCount = 1

treeCount = slope(1,1)
factorTreeCount = factorTreeCount * treeCount

treeCount = slope(3,1)
factorTreeCount = factorTreeCount * treeCount

treeCount = slope(5,1)
factorTreeCount = factorTreeCount * treeCount

treeCount = slope(7,1)
factorTreeCount = factorTreeCount * treeCount

treeCount = slope(1,2)
factorTreeCount = factorTreeCount * treeCount

print()
print(f"result part 2 = {factorTreeCount}")