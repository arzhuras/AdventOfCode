import time


def transform_position(transfo, position):
    return [
        transfo[0] * position[0] + transfo[1] * position[1] + transfo[2] * position[2],
        transfo[3] * position[0] + transfo[4] * position[1] + transfo[5] * position[2],
        transfo[6] * position[0] + transfo[7] * position[1] + transfo[8] * position[2],
    ]


def cos(i):
    if i == 0:
        return 1
    if i == 180:
        return -1
    return 0


def sin(i):
    if i == 90:
        return 1
    if i == 270:
        return -1
    return 0


class Scanner:
    def __init__(self, i):
        self.id = i
        self.transfo = [1, 0, 0, 0, 1, 0, 0, 0, 1]
        self.position = [0, 0, 0]
        self.beacons = []
        self.matched = False

    def add_beacon(self, beacon):
        self.beacons.append(beacon)

    def get_beacons_real_coords(self):
        b = []
        for beacon in self.beacons:
            b_rot = transform_position(self.transfo, beacon)
            new_pos = [b_rot[0] + self.position[0], b_rot[1] + self.position[1], b_rot[2] + self.position[2]]
            b.append(new_pos)
        return b

    def get_beacon_coord(self, beacon):
        new_pos = transform_position(self.transfo, beacon)
        new_pos = [new_pos[0] + self.position[0], new_pos[1] + self.position[1], new_pos[2] + self.position[2]]
        return new_pos

    def set_origin_by_matching(self, real_beacon_pos, beacon_relative):
        # real - rel * transfo
        b_rot = transform_position(self.transfo, beacon_relative)
        origin = [real_beacon_pos[0] - b_rot[0], real_beacon_pos[1] - b_rot[1], real_beacon_pos[2] - b_rot[2]]
        self.position = origin


def try_match(scan_a, scan_b, transfos):
    set_a = set(tuple(i) for i in scan_a.get_beacons_real_coords())
    for transfo in transfos:
        scan_b.transfo = transfo
        for real_beacon_a in set_a:
            for beacon_b in scan_b.beacons:
                # We want to put beacon_b on beacon_a
                scan_b.set_origin_by_matching(real_beacon_a, beacon_b)
                set_b = set(tuple(i) for i in scan_b.get_beacons_real_coords())
                if len(set_a.intersection(set_b)) >= 12:
                    scan_b.matched = True
                    print("Match!")
                    return


def main():
    with open("input.txt", "r") as in19:
        lines = [line.strip() for line in in19.readlines()]
    s = time.time()

    scans = []
    for line in lines:
        if "scanner" in line:
            scan = Scanner(int(line.split(" ")[2]))
            scans.append(scan)
            continue

        if "," in line:
            beacon = [int(x) for x in line.split(",")]
            scans[-1].add_beacon(beacon)

    transfos = set()
    for c in [0, 90, 180, 270]:  # X
        for b in [0, 90, 180, 270]:  # Y
            for a in [0, 90, 180, 270]:  # Z
                rot = (
                    cos(a) * cos(b),
                    cos(a) * sin(b) * sin(c) - sin(a) * cos(c),
                    cos(a) * sin(b) * cos(c) + sin(a) * sin(c),
                    sin(a) * cos(b),
                    sin(a) * sin(b) * sin(c) + cos(a) * cos(c),
                    sin(a) * sin(b) * cos(c) - cos(a) * sin(c),
                    -sin(b),
                    cos(b) * sin(c),
                    cos(b) * cos(c),
                )
                transfos.add(rot)

    scans[0].matched = True
    while sum([0 if scan.matched else 1 for scan in scans]) > 0:
        print(f"Matched {sum([1 if scan.matched else 0 for scan in scans])}/{len(scans)} scans")
        for i in range(0, len(scans)):
            for j in range(i + 1, len(scans)):
                if scans[i].matched and (not scans[j].matched):
                    try_match(scans[i], scans[j], transfos)
                if scans[j].matched and (not scans[i].matched):
                    try_match(scans[j], scans[i], transfos)

    beacons = set()
    for scan in scans:
        b = scan.get_beacons_real_coords()
        beacons.update(set(tuple(i) for i in b))
    print("Part 1:", len(beacons))

    max_man_dist = 0
    for i in range(0, len(scans)):
        for j in range(i + 1, len(scans)):
            x = abs(scans[i].position[0] - scans[j].position[0])
            y = abs(scans[i].position[1] - scans[j].position[1])
            z = abs(scans[i].position[2] - scans[j].position[2])
            max_man_dist = max(max_man_dist, x + y + z)

    print("part 2:", max_man_dist)
    print(f"Took {time.time() - s:.3f}s")


if __name__ == "__main__":
    main()
