import datetime
import os
import sys

import requests
from bs4 import BeautifulSoup

""" 
- Se logguer sur https://adventofcode.com/
- <ctrl> + <shift> + i
- onglet stockage
- groupe Cookies
- cooikie: session 
-> recopier la valeur dans .session
"""
SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])
os.chdir(SCRIPT_DIR)

print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")

ANSI_NORM = "\033[0m"
ANSI_RED = "\033[31;1m"
ANSI_GREEN = "\033[32;1m"
ANSI_BLUE = "\033[34;1m"

SESSION_FILE_NAME = ".session"
TEMPLATE_FILE_NAME = "template.py"

URL_DAY = "https://adventofcode.com/{0}/day/{1}"
URL_INPUT = URL_DAY + "/input"

print(sys.argv, len(sys.argv))

targetDay = ""
if len(sys.argv) >= 2:
    targetDay = sys.argv[1]

targetYear = ""
if len(sys.argv) >= 3:
    targetYear = sys.argv[2]

if not os.path.exists(SESSION_FILE_NAME):
    print(ANSI_RED, "Missing .session file ", ANSI_NORM)
    exit()

with open(SESSION_FILE_NAME, "r") as inputFile:
    session = inputFile.read().strip()

if len(session) != 128:
    print(
        ANSI_RED,
        "invalid session cookie in .session file (bad length <> 128) :",
        len(session),
        session,
        ANSI_NORM,
        session,
    )
    exit()
print("session token:", session)

s = requests.session()
# s.cookies.set("session", session, domain=".adventofcode.com")
s.cookies.set("session", session)

date = datetime.date.today()

if targetDay == "":
    targetDay = str(date.day)
targetDay = int(targetDay)

if targetYear == "":
    targetYear = str(date.year)
targetYear = int(targetYear)

# print(f"{targetDay} {targetYear} {URL_DAY.format(targetYear, targetDay)}")

# Get current day puzzle
r = s.get(URL_DAY.format(targetYear, targetDay))

if r.status_code != 200:
    print()
    print(ANSI_RED, "Invalid date", targetDay, targetYear, ANSI_NORM)
    print("USAGE:", sys.argv[0], "<DAY> <YEAR>")
    print()
    exit()
# print(r.text)
soup = BeautifulSoup(r.text, "html.parser")

dayTitle = soup.find("h2").text
dayTitle = dayTitle.replace("-", "")
dayTitle = dayTitle.replace("Day", "")
dayTitle = dayTitle.replace(str(targetDay), "")
dayTitle = dayTitle.replace(":", "")
dayTitle = dayTitle.replace("?", "")
dayTitle = dayTitle.replace("!", "")
dayTitle = dayTitle.strip()
# _, _, dayTitle = dayTitle.split()
# print(dayTitle)

# Create current day directory
DAY_PATH = f"{targetYear}/{targetDay:02} - {dayTitle}"
# print(f"### {targetDay:02} {targetDay} {DAY_PATH}")
print(ANSI_BLUE, DAY_PATH, ANSI_NORM)
os.makedirs(DAY_PATH, exist_ok=True)

# sample input: a <code> imbeded in a <pre>
codeLst = [preLst.find("code") for preLst in soup.findAll("pre")]

print(ANSI_BLUE, "  sample.txt", ANSI_NORM)
with open(f"{DAY_PATH}/sample.txt", "w") as destFile:
    destFile.write(codeLst[0].text)

# Get current day input
r = s.get(URL_INPUT.format(targetYear, targetDay))
# print(r.text)

print(ANSI_BLUE, "  input.txt", ANSI_NORM)
with open(f"{DAY_PATH}/input.txt", "w") as destFile:
    destFile.write(r.text)

destFileName = f"AoC_{targetYear}_{targetDay}.py"
if os.path.exists(f"{DAY_PATH}/{destFileName}"):
    print(ANSI_RED, f"{DAY_PATH}/{destFileName} already exists", ANSI_NORM)
    exit()
print(ANSI_BLUE, f"  {destFileName}", ANSI_NORM)
with open(TEMPLATE_FILE_NAME, "r") as inputFile, open(
    f"{DAY_PATH}/{destFileName}", "x"
) as destFile:
    content = inputFile.read()
    destFile.write(content)
