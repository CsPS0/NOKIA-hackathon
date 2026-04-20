import re
from pathlib import Path
from typing import Optional

def next_magic_num(s: str) -> Optional[str]:
    s = s.strip()
    if not s: 
        return None
        

    match = re.match(r"^\s*(\d+)\s*(?:\^\s*(\d+)\s*)?$", s)
    if not match:
        raise ValueError(f"Invalid input format: {s}")
        
    base_str = match.group(1)
    exp_str = match.group(2)
    
    if exp_str:
        val = int(base_str) ** int(exp_str)
        s = str(val)
    else:
        s = str(int(base_str))
        
    L = len(s)
    L_half = (L + 1) // 2
    left_str = s[:L_half]
    
    cand_str = left_str + (left_str[-2::-1] if L % 2 != 0 else left_str[::-1])
    
    if int(cand_str) > int(s):
        return cand_str
    
    left = int(left_str)
    new_left = str(left + 1)
    
    if len(new_left) > L_half:
        return '1' + '0' * (L - 1) + '1'
    else:
        return new_left + (new_left[-2::-1] if L % 2 != 0 else new_left[::-1])

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
        try:
            res = next_magic_num(line)
            print(f"next_magic_num({line}) => {res}")
        except ValueError as e:
            print(f"Error parsing line: {e}")

if __name__ == "__main__":
    main()
