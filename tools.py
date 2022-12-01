import sys
import os

SCRIPT_DIR = os.path.dirname(sys.argv[0])
SCRIPT_NAME = os.path.basename(sys.argv[0])


class Ansi:
    """Code couleur Ansi"""

    norm = "\033[0m"
    grey = "\033[30;1m"
    red = "\033[31;1m"
    green = "\033[32;1m"
    yellow = "\033[33;1m"
    blue = "\033[34;1m"
    purple = "\033[35;1m"
    cyan = "\033[36;1m"


def init_script():
    os.chdir(SCRIPT_DIR)

    print(f"=== {SCRIPT_DIR}/{SCRIPT_NAME} ===")


if __name__ == "__main__":
    init_script()
    print(Ansi.green, __name__, Ansi.norm)
    ansi = Ansi()
    ansi.toto = "zorro"
    print(ansi.toto)
