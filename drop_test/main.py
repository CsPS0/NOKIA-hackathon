import math
from pathlib import Path

def min_num_of_drops(n: int, h: int) -> int:

    if h <= 0 or n <= 0:
        return 0

    low, high = 1, h
    while low < high:
        mid = (low + high) // 2
        total_floors = sum(math.comb(mid, i) for i in range(1, n + 1))
        
        if total_floors >= h:
            high = mid
        else:
            low = mid + 1
            
    return low

def main() -> None:
    input_file = Path(__file__).parent / "input.txt"
    if not input_file.exists():
        print("input.txt not found.")
        return
        
    data = input_file.read_text(encoding="utf-8").splitlines()
    for line in data:
        line = line.strip()
        if not line: 
            continue
        parts = line.split(',')
        if len(parts) == 2:
            n = int(parts[0].strip())
            h = int(parts[1].strip())
            res = min_num_of_drops(n, h)
            print(f"min_num_of_drops({n}, {h}) => {res}")

if __name__ == "__main__":
    main()
