import sys, os
import timeit
import re 

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

INPUT_FILE_NAME = SCRIPT_NAME.replace("py","txt")
print (f"=== {SCRIPT_NAME} ===")

def passport():
    keyLabel = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]

    validPassportCount = 0
    invalidPassportCount = 0
    fieldCount = 0
    invalidFieldCount = 0
    blankLineCount = 0
    cidFieldPresent = False
    with open(INPUT_FILE_NAME, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            if (len(line) == 0) :
                blankLineCount = blankLineCount + 1
                if (fieldCount == 8 or (fieldCount == 7 and cidFieldPresent == False)):
                    print("VALID", fieldCount, cidFieldPresent, invalidFieldCount, blankLineCount)
                    validPassportCount = validPassportCount + 1
                else :
                    invalidPassportCount = invalidPassportCount + 1
                    print("INVALID PASSPORT", fieldCount, cidFieldPresent, invalidFieldCount, blankLineCount)
                fieldCount = 0
                #invalidFieldCount = 0
                cidFieldPresent = False
                print()
                continue
            print(">",line)
            for field in line.split():
                key, value = field.split(sep = ":")
                #print ("=",field, key, value)
                if (key not in keyLabel):
                    invalidFieldCount = invalidFieldCount + 1
                    print("INVALID KEY", key)
                    continue

                if (key == "cid"):
                    cidFieldPresent = True
                fieldCount = fieldCount + 1

    print(f"- passport() = {validPassportCount}, {invalidPassportCount}")
    return validPassportCount

def passport2():
    keyLabel = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    eclLabel = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    validPassportCount = 0
    invalidPassportCount = 0
    fieldCount = 0
    invalidFieldCount = 0
    blankLineCount = 0
    cidFieldPresent = False
    with open(INPUT_FILE_NAME, "r") as inputFile:
        for line in inputFile:
            line = line.rstrip("\n")
            if (len(line) == 0) :
                blankLineCount = blankLineCount + 1
                if (fieldCount == 8 or (fieldCount == 7 and cidFieldPresent == False)):
                    print("VALID", fieldCount, cidFieldPresent, invalidFieldCount, blankLineCount)
                    validPassportCount = validPassportCount + 1
                else :
                    invalidPassportCount = invalidPassportCount + 1
                    print("INVALID PASSPORT", fieldCount, cidFieldPresent, invalidFieldCount, blankLineCount)
                fieldCount = 0
                #invalidFieldCount = 0
                cidFieldPresent = False
                print()
                continue
            print(">",line)
            for field in line.split():
                key, value = field.split(sep = ":")
                #print ("=",field, key, value)
                if (key not in keyLabel):
                    invalidFieldCount = invalidFieldCount + 1
                    print("INVALID KEY", key)
                    continue

                if (key == "byr" and len(value) == 4 and (int(value) < 1920 or int(value) > 2002)):
                    invalidFieldCount = invalidFieldCount + 1
                    print("INVALID KEY", field)
                    continue

                if (key == "iyr" and len(value) == 4 and (int(value) < 2010 or int(value) > 2020)):
                    invalidFieldCount = invalidFieldCount + 1
                    print("INVALID KEY", field)
                    continue

                if (key == "eyr" and len(value) == 4 and (int(value) < 2020 or int(value) > 2030)):
                    invalidFieldCount = invalidFieldCount + 1
                    print("INVALID KEY", field)
                    continue

                if (key == "ecl" and value not in eclLabel):
                    invalidFieldCount = invalidFieldCount + 1
                    print("INVALID KEY", field)
                    continue

                if (key == "hcl" and not re.search("^#[0-9a-f]{6}$", value)):
                    invalidFieldCount = invalidFieldCount + 1
                    print("INVALID KEY", field)
                    continue

                if (key == "pid" and not re.search("^\d{9}$", value)):
                    invalidFieldCount = invalidFieldCount + 1
                    print("INVALID KEY", field)
                    continue

                if (key == "hgt"):
                    if (re.search("^\d{2}in$", value)):
                        value = value.replace("in", "")
                        if (int(value) < 59 or int(value) > 76):
                            invalidFieldCount = invalidFieldCount + 1
                            print("INVALID KEY in", field)
                            continue
                    elif (re.search("^\d{3}cm$", value)):
                        value = value.replace("cm", "")
                        if (int(value) < 150 or int(value) > 193):
                            invalidFieldCount = invalidFieldCount + 1
                            print("INVALID KEY cm", field)
                            continue
                    else :
                        invalidFieldCount = invalidFieldCount + 1
                        print("INVALID KEY", field)
                        continue

                if (key == "cid"):
                    cidFieldPresent = True
                fieldCount = fieldCount + 1

    print(f"- passport() = {validPassportCount}, {invalidPassportCount}")
    return validPassportCount

###
### PART 1
###

print()
print(f"### PART 1 ###")

passportCount = passport()

print()
print(f"result part 1 = {passportCount}")

###
### PART 2
###

print()
print(f"### PART 2 ###")

passportCount = passport2()

print()
print(f"result part 2 = {passportCount}")