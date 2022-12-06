from collections import deque
from pathlib import Path


def find_start_byte(stream: str, length: int = 4) -> int:
    buffer = deque(maxlen=length)
    for i, byte in enumerate(stream, start=1):
        buffer.append(byte)
        if len(set(buffer)) == length:
            return i


def main():
    text = Path("../inputs/day_06.txt").read_text()
    print(f"Part 1: {find_start_byte(text)}")
    print(f"Part 2: {find_start_byte(text, length=14)}")


if __name__ == "__main__":
    main()
