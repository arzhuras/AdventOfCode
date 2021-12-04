import sys, os
import timeit
import requests


SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_NAME} ===")

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
INPUT_URL = "https://adventofcode.com/2021/day/" + 1 + "/input"

g_inputLines = []


def readInputFile(argFile=INPUT_FILE_NAME):

    # if input file not present, get it from the web
    if (! os.path.exists(argFile)):
        r = requests.get(INPUT_URL)
        r.text

    inputLines = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines


g_inputLines = readInputFile()

print(g_inputLines)
