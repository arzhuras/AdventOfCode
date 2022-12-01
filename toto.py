#AOC 2022 Day 1
elves = open("toto.txt").read().split("\n\n")
#print(elves)
calories = [sum(map(int, elf.split())) for elf in elves]
print(max(calories), sum(sorted(calories)[-3:]))