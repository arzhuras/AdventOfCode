import sys
import os
import time
import re
import copy
import math

from collections import namedtuple

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py", "txt")
print(f"=== {SCRIPT_NAME} ===")


def readInputFile(file=INPUT_FILE_NAME):
    'read the input file'

    inputLines = []
    print(f"-> read {file}")
    with open(file, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            inputLines.append(line)
    return inputLines


g_inputLines = []
g_data_d = {}
INGREDIENT = 0
ALLERGEN = 1

#g_cmd_nt = namedtuple('cmd', ['name', 'arg1', 'arg2'])

def initDataStructure():
    global g_data_d

    g_data_d = {}
    g_data_d['foods'] = []

    # https://pythex.org/
    #patternRule = r"^(\d*): (\d*) (\d*) \| (\d*)-(\d*)"
    for i in range(len(g_inputLines)):
        line = g_inputLines[i]
        #print(line)
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace(',', '')
        fields = line.split()

        g_data_d['foods'].append([[], []])
        ingredient_l = g_data_d['foods'][i][INGREDIENT]
        allergen_l = g_data_d['foods'][i][ALLERGEN]
        #print(ingredient_l, allergen_l)

        part2 = False
        for field in fields:
            if (field == "contains"):
                part2 = True
                continue

            if (part2 == False):
                ingredient_l.append(field)
            else:
                allergen_l.append(field)
    #print(g_data_d['foods'])

def resolve_part2():
    # print("resolve_part2():", g_data_d}

    return -1


def resolve_part1():
    #print("resolve_part1():", g_data_d)
    toto = 1
    '''
    for i in range(len(g_data_d['foods'])):
        print("->", i)
        print(" ", g_data_d['foods'][i][INGREDIENT])
        print(" ", g_data_d['foods'][i][ALLERGEN])
    '''
    food_l = copy.deepcopy(g_data_d['foods'])

    # on boucle sur la liste jusqu'a épuiser tous les allergen
    allergen_d = {}
    round = 1
    maxRound = 10
    foodLen = len(food_l)
    while (round <= maxRound):
        #print("food_l", food_l)
        print()
        print("###### ROUND", round, "#########")

        # on parcours tous les allergens uniques
        maxFood = len(food_l)
        foodIdx = 0

        while foodIdx < maxFood:
            food = food_l[foodIdx]
            print()
            #print(f"food: [{foodIdx}] {food}")
            if (len(food[ALLERGEN]) > 1):
                print(f"NOT UNIQUE {foodIdx} {food[ALLERGEN]}")
                foodIdx += 1
                maxFood = len(food_l)
                continue

            allergen = food[ALLERGEN][0]

            print(f"UNIQUE {foodIdx} {allergen:6} #ingredients {len(food[INGREDIENT])}")
            if (round > 2):
                print(f"{food[INGREDIENT]}")
    
            # on elimine les impossibles dans le food unique en cherchant dans toute la liste
            tmp_i = len(food[INGREDIENT])
            for foodIdx2 in range(len(food_l)):
                food2 = food_l[foodIdx2]
                tmp_l = []
                for ingredient in food[INGREDIENT]:
                    if (allergen in food2[ALLERGEN] and ingredient not in food2[INGREDIENT]):
                        tmp_l.append(ingredient)
                #print("  food2:", food2, tmp_l)

                if (len(tmp_l) > 0):
                    for ingredient in tmp_l:
                        food[INGREDIENT].remove(ingredient)
                    #print(f"  cleaned {foodIdx} {foodIdx2}", food, tmp_l)
            if (tmp_i != len(food[INGREDIENT])):
                print(f"  cleaned {foodIdx} {food}")

            # nettoyage si unique
            if (len(food[INGREDIENT]) == 1):
                print("BINGO", allergen, food[INGREDIENT])
                allergen_d[allergen] = food[INGREDIENT][0]
                food_l.pop(foodIdx)
                
                foodIdx2 = 0
                maxFood2 = len(food_l)
                while foodIdx2 < maxFood2:
                    food2 = food_l[foodIdx2]
                    #print("food_l:", food_l)
                    #print("food2:", foodIdx2, food2)
                    if (allergen in food2[ALLERGEN]):
                        #print(f"  match allergen: [{foodIdx2}]{food2}")
                        if (len(food2[ALLERGEN]) == 1): # duplicat, on le supprime aussi!
                            #print("  DUPLICATE", foodIdx, foodIdx2)
                            food_l.pop(foodIdx2)
                            if (foodIdx2 < foodIdx):
                                foodIdx -= 1
                                foodIdx2 -= 1
                        else:
                            food2[ALLERGEN].remove(allergen)
                            #print(f"    cleaned allergen: [{foodIdx2}] {food2}")
                    if (allergen_d[allergen] in food2[INGREDIENT]):
                            food2[INGREDIENT].remove(allergen_d[allergen])
                            #print(f"  cleaned ingredient: [{foodIdx2}] {food2}")
                    #print("foodl:", food_l)
                    foodIdx2 += 1
                    maxFood2 = len(food_l)
            #print("food_l", food_l)

            foodIdx += 1
            maxFood = len(food_l)
        
        #nettoyage des allergens terminés
        if (len(food_l) == 0):
            round = maxRound
        round += 1

        print(allergen_d)
        print(f"LOOP {round} remain {len(food_l)}")

        if (foodLen == len(food_l)):
            print("INFINITE LOOP DETECTED -> STOP")
            round = maxRound + 1
            #exit()
        foodLen = len(food_l)

    # compte les ingredient sans allergen
    tmp_l = allergen_d.values()
    res1 = 0
    for food in g_data_d['foods']:
        for ingredient in food[INGREDIENT]:
            if (ingredient not in tmp_l):
                res1 += 1
    
    #part 2: canonical dangerous ingredient list
    res2 = ""
    for allergen in sorted(allergen_d.keys()):
        res2 += allergen_d[allergen] + ","
    res2 = res2[:-1]
    return (res1, res2)


#g_inputLines = readInputFile("AoC_2020_21_sample.txt")
g_inputLines = readInputFile()

res = -1

###
# PART 1
###

#'''
print()
print(f"### PART 1 ###")

tic = time.perf_counter()

initDataStructure()
res = resolve_part1()

toc = time.perf_counter()

print(f"-> result part 1 = {res[0]}")
print(f"-> result part 2 = {res[1]}")
print(f"{toc - tic:0.4f} seconds")
#'''

###
# PART 2
###

'''
print()
print(f"### PART 2 ###")

tic = time.perf_counter()

#initDataStructure()
res = resolve_part2()

toc = time.perf_counter()

print(f"-> result part 2 = {res}")
print(f"{toc - tic:0.4f} seconds")
'''
