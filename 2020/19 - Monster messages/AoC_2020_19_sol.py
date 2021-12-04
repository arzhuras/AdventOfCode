def match(string, stack):
    if len(stack) > len(string):
        return False
    elif len(stack) == 0 or len(string) == 0:
        return len(stack) == 0 and len(string) == 0
    
    c = stack.pop()
    if isinstance(c, str):
        if string[0] == c:
            return match(string[1:], stack.copy())
    else:
        for rule in rules[c]:
            if match(string, stack + list(reversed(rule))):
                return True
    return False


def valid_messages():
    total = 0
    for message in messages:
        if match(message, list(reversed(rules[0][0]))):
            total += 1
    return total


with open('AoC_2020_19_sample3.txt') as file:
    rules_raw, messages = tuple(map(lambda x: x.splitlines(), file.read().split('\n\n')))

rules = {}
for rule_raw in rules_raw:
    num, contents = rule_raw.split(': ')
    if contents[0] == '"':
        rules[int(num)] = contents[1]
    else:
        rules[int(num)] = list(map(lambda x: list(map(int, x.split(' '))), contents.split(' | ')))
print(rules)

print("Part 1:", valid_messages())
rules[8] = [[42], [42, 8]]
rules[11] = [[42, 31], [42, 11, 31]]
print("Part 2:", valid_messages())
