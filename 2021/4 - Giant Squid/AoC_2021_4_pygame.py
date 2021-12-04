import sys
import os
import time
import pygame
import glob
from PIL import Image

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

ANSI_NORM = "\033[0m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
# INPUT_URL = "https://adventofcode.com/2021/day/" + str(1) + "/input"


g_inputLines = []
g_data = {}

#############################
### INITIALISATION & DATA ###
#############################

# Graphical parameters
NB_GRID = 10
NB_CELL = 5
MARGIN_OUT = 5
MARGIN_IN = 5
CELL_WIDTH = 10
CELL_PAD = 2

COLOR_BOARD = (200, 200, 200)
COLOR_CELL = (88, 163, 232)
COLOR_CELL_MARKED = (201, 142, 52)
COLOR_CELL_WON = (201, 0, 0)

BOARD_WIDTH = 2 * MARGIN_IN + NB_CELL * CELL_WIDTH + (NB_CELL - 1) * CELL_PAD
TOTAL_WIDTH = MARGIN_OUT + BOARD_WIDTH


def readInputFile(argFile=INPUT_FILE_NAME):
    inputLines = []
    print(f"-> read {argFile}")
    with open(argFile, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    print(f"  {len(inputLines)} lignes")
    # print(inputLines)
    return inputLines


def initData():
    g_data["raw"] = [int(field) for field in g_inputLines[0].split(",")]

    curLine = 2
    g_data["grid"] = []
    while curLine < len(g_inputLines):
        grid = []
        for j in range(5):
            grid.append([int(field) for field in g_inputLines[curLine + j].split()])
        g_data["grid"].append(grid)
        curLine += 6

    # print(g_data)


##################
### PROCEDURES ###
##################


def waitSpacePress():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                return


def drawCell(gridId, line, col, color):

    # print("gridId", gridId, "line", line, "col", col)
    gridLine = int(gridId / NB_GRID)
    gridCol = gridId % NB_GRID
    # print(gridId, gridLine, gridCol)

    curOffsetY = gridLine * TOTAL_WIDTH
    curOffsetX = gridCol * TOTAL_WIDTH

    pygame.draw.rect(
        surf,
        color,
        (
            curOffsetX + MARGIN_OUT + MARGIN_IN + col * (CELL_WIDTH + CELL_PAD),
            curOffsetY + MARGIN_OUT + MARGIN_IN + line * (CELL_WIDTH + CELL_PAD),
            CELL_WIDTH,
            CELL_WIDTH,
        ),
    )

    pygame.display.flip()
    # waitSpacePress()


def writeCell(gridId, text):
    gridLine = int(gridId / NB_GRID)
    gridCol = gridId % NB_GRID

    curOffsetY = gridLine * TOTAL_WIDTH
    curOffsetX = gridCol * TOTAL_WIDTH

    color = (200, 200, 200)
    if text == 1 or text == 100:
        color = (25, 200, 20)
    pygame.draw.rect(
        surf,
        color,
        (
            curOffsetX + MARGIN_OUT + MARGIN_IN + 13,
            curOffsetY + MARGIN_OUT + MARGIN_IN + 20,
            38,
            22,
        ),
    )

    myfont = pygame.font.SysFont("Comic Sans MS", 20, bold=True, italic=False)
    # myfont = pygame.font.SysFont("Courier New", 20)
    textsurface = myfont.render(f"{text:3}", False, (0, 0, 0))
    surf.blit(textsurface, (curOffsetX + 22, curOffsetY + 25))

    pygame.display.flip()


def initGraphicalBoard():  # 10 x 10
    surf.fill((0, 0, 0))

    for line in range(NB_GRID):
        curOffsetY = line * TOTAL_WIDTH
        for col in range(NB_GRID):
            curOffsetX = col * TOTAL_WIDTH

            # draw board
            pygame.draw.rect(
                surf,
                COLOR_BOARD,
                (
                    curOffsetX + MARGIN_OUT,
                    curOffsetY + MARGIN_OUT,
                    BOARD_WIDTH,
                    BOARD_WIDTH,
                ),
            )

            # draw cells
            for i in range(NB_CELL):
                for j in range(NB_CELL):
                    pygame.draw.rect(
                        surf,
                        COLOR_CELL,
                        (
                            curOffsetX + MARGIN_OUT + MARGIN_IN + i * (CELL_WIDTH + CELL_PAD),
                            curOffsetY + MARGIN_OUT + MARGIN_IN + j * (CELL_WIDTH + CELL_PAD),
                            CELL_WIDTH,
                            CELL_WIDTH,
                        ),
                    )

    pygame.display.flip()


def isWin(gridId, raw):
    grid = g_data["grid"][gridId]
    for line in range(5):
        for col in range(5):
            if grid[line][col] == raw:
                grid[line][col] = -1
                # print(raw, gridId, grid)
                drawCell(gridId, line, col, COLOR_CELL_MARKED)
            # print(sum(grid[line]), grid[line])
            if sum(grid[line]) == -5:
                grid[0][0] = -2  # mark as already won
                for i in range(NB_CELL):
                    drawCell(gridId, line, i, COLOR_CELL_WON)
                return True
            elif sum([grid[i][col] for i in range(5)]) == -5:
                grid[0][0] = -2  # mark as already won
                for i in range(NB_CELL):
                    drawCell(gridId, i, col, COLOR_CELL_WON)
                return True
    return False


def scanGrid():
    winGridLst = []
    for rawId in range(len(g_data["raw"])):
        raw = g_data["raw"][rawId]
        for gridId in range(len(g_data["grid"])):
            grid = g_data["grid"][gridId]
            if grid[0][0] == -2:  # skip grid already won
                continue

            if isWin(gridId, raw) == True:
                winGridLst.append([gridId, raw, sumUnmarked(grid)])
                writeCell(gridId, len(winGridLst))
                print("GOTCHA -", "gridId:", gridId, "winGridLst[-1]:", winGridLst[-1])
        pygame.image.save(surf, f"png\screenshot{rawId:03}.png")

    return winGridLst


def sumUnmarked(grid):
    score = 0
    for line in grid:
        for elt in line:
            if elt > -1:
                score += elt
    return score


def resolve_part1(winGrid):
    print()
    print(ANSI_RED, "### PART 1 ###", ANSI_NORM)

    print("first win grid:", winGrid[0])
    print(g_data["grid"][winGrid[0]])
    print("raw:", winGrid[1], "unmarked sum:", winGrid[2])

    return winGrid[1] * winGrid[2]


def resolve_part2(winGrid):
    print()
    print(ANSI_RED, "### PART 2 ###", ANSI_NORM)

    print("last win grid:", winGrid[0])
    print(g_data["grid"][winGrid[0]])
    print("raw:", winGrid[1], "unmarked sum:", winGrid[2])

    return winGrid[1] * winGrid[2]


############
### MAIN ###
############


# g_inputLines = readInputFile("sample.txt")
g_inputLines = readInputFile("AoC_2021_4.txt")

initData()

surf = pygame.display.set_mode((735, 735))
pygame.font.init()  # you have to call this at the start, if you want to use this module.
initGraphicalBoard()

startTime = time.time()
winGridLst = scanGrid()  # winGrid: id, raw, unmarked sum
print()
print(f"-> scan grid ({time.time() - startTime:.3f}s)")

frames = []
imgs = glob.glob("png\*.png")
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save("animated.gif", format="GIF", append_images=frames[1:], save_all=True, duration=70, loop=0)

startTime = time.time()
res = resolve_part1(winGridLst[0])
print()
print(f"-> part 1 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

startTime = time.time()
res = resolve_part2(winGridLst[-1])
print()
print(f"-> part 2 ({time.time() - startTime:.3f}s): {ANSI_BLUE}{res}{ANSI_NORM}")

print(len(g_data["raw"]))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
