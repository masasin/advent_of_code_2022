from collections import defaultdict
from pathlib import Path


data = defaultdict(int)


path = Path("/")
for line in open("../inputs/day_07.txt").readlines():
    match line.strip().split():
        case ["$", "cd", ".."]:
            path = path.parent
        case ["$", "cd", subdir]:
            path /= subdir
        case ["$" | "dir", _]:
            pass
        case [size, name]:
            file = path / name
            size = int(size)
            for parent in file.parents:
                data[parent] += size


sizes = data.values()
print(sum(v for v in sizes if v <= 100_000))
print(min(v for v in sizes if v >= (data[Path("/")] - 40_000_000)))
