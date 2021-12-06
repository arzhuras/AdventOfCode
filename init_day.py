import sys
import os
from bs4 import BeautifulSoup
import requests
import datetime

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


if not os.path.exists(SESSION_FILE_NAME):
    print(ANSI_RED, "Missing .session file ", ANSI_NORM)
    exit()

with open(SESSION_FILE_NAME, "r") as inputFile:
    session = inputFile.read()

if len(session) != 96:
    print(ANSI_RED, "invalid session cookie:", ANSI_NORM, session)
    exit()
print("session token:", session)

s = requests.session()
# s.cookies.set("session", session, domain=".adventofcode.com")
s.cookies.set("session", session)

date = datetime.date.today()


# Get current day puzzle
r = s.get(URL_DAY.format(date.year, date.day))
# print(r.text)
soup = BeautifulSoup(r.text, "html.parser")

dayTitle = soup.find("h2").text
dayTitle = dayTitle.replace("-", "")
dayTitle = dayTitle.strip()
_, _, dayTitle = dayTitle.split()
# print(dayTitle)

# Create current day directory
DAY_PATH = f"{date.year}.bak/{date.day} - {dayTitle}"
print(ANSI_BLUE, DAY_PATH, ANSI_NORM)
os.makedirs(DAY_PATH, exist_ok=True)

# sample input: a <code> imbeded in a <pre>
codeLst = [preLst.find("code") for preLst in soup.findAll("pre")]

print(ANSI_BLUE, "  sample.txt", ANSI_NORM)
with open(f"{DAY_PATH}/sample.txt", "w") as destFile:
    destFile.write(codeLst[0].text)

# Get current day input
r = s.get(URL_INPUT.format(date.year, date.day))
# print(r.text)

print(ANSI_BLUE, "  input.txt", ANSI_NORM)
with open(f"{DAY_PATH}/input.txt", "w") as destFile:
    destFile.write(r.text)

tmp = f"AoC_{date.year}_{date.day}.py"
print(ANSI_BLUE, f"  {tmp}.txt", ANSI_NORM)
with open(TEMPLATE_FILE_NAME, "r") as inputFile, open(f"{DAY_PATH}/{tmp}", "w") as destFile:
    content = inputFile.read()
    destFile.write(content)
