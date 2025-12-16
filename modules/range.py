from tools import *


# arg range1: (start , end, span) range2: (start , end, span), pas forcément dans l'ordre
# return: range overlap, range before, range after
# return None if range is empty
def getOverlapRange(range1: tuple, range2: tuple) -> tuple:

    if range1[0] < range2[0] and range1[1] < range2[0]:
        return None, range1, range2  # disjoint
    if range2[0] < range1[0] and range2[1] < range1[0]:
        return None, range2, range1  # disjoint inversé

    start = max(range1[0], range2[0])
    end = min(range1[1], range2[1])
    rangeOverlap = (start, end, end - start + 1)

    rangeBefore = None
    if range1[0] != range2[0]:
        start = min(range1[0], range2[0])
        end = rangeOverlap[0] - 1
        rangeBefore = (start, end, end - start + 1)

    rangeAfter = None
    if range1[1] != range2[1]:
        start = rangeOverlap[1] + 1
        end = max(range1[1], range2[1])
        rangeAfter = (start, end, end - start + 1)

    return rangeOverlap, rangeBefore, rangeAfter


def checkOverlap(range1, range2, overlap, before, after):
    if (
        (overlap[2] if overlap is not None else 0) * 2
        + (before[2] if before is not None else 0)
        + (after[2] if after is not None else 0)
    ) != (range1[2] + range2[2]):
        print(
            "bef",
            before,
            "over",
            overlap,
            "aft",
            after,
            (overlap[2] if overlap is not None else 0) * 2
            + (before[2] if before is not None else 0)
            + (after[2] if after is not None else 0),
        )
        print(range1, range2, range1[2] + range2[2])
        print("ERREUR DE CALCUL DES SPANS")
        exit()


def showGetOverlap(range1, range2, overlap, before, after):
    print(
        f"[{range1[0]}, {range1[1]}] = {range1[2]} / [{range2[0]}, {range2[1]}] = {range2[2]} -> ",
        end="",
    )
    if before is not None:
        print(f"[{before[0]}, {before[1]}] = {before[2]}, ", end="")
    else:
        print("NONE, ", end="")
    if overlap is not None:
        print(f"[{overlap[0]}, {overlap[1]}] = {overlap[2]}, ", end="")
    else:
        print("NONE, ", end="")
    if after is not None:
        print(f"[{after[0]}, {after[1]}] = {after[2]}")
    else:
        print("NONE")


if __name__ == "__main__":
    init_script()

    # test_overlap()
    for elt1, elt2 in (
        [(1, 3), (2, 4)],  # A cheval
        [(2, 4), (1, 3)],
        [(1, 3), (3, 5)],  # Bord à bord
        [(3, 5), (1, 3)],
        [(1, 5), (2, 4)],  # Milieux
        [(2, 4), (1, 5)],
        [(1, 3), (1, 5)],  # Limite gauche
        [(1, 5), (1, 3)],
        [(3, 5), (1, 5)],  # Limite droite
        [(1, 5), (3, 5)],
        [(1, 5), (1, 5)],  # Identique
        [(1, 2), (3, 4)],  # Disjoint
        [(3, 4), (1, 2)],
    ):
        print(elt1, elt2, getOverlapRange(elt1, elt2))
