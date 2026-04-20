import csv
import math
from datetime import datetime
from pathlib import Path
from typing import Union


FREE_MINUTES = 30
HOURLY_RATE_1 = 300
HOURLY_RATE_1_LIMIT_MINUTES = 180
HOURLY_RATE_2 = 500
DAILY_CAP = 10000
MINUTES_IN_DAY = 1440

def calculate_fee(entry_str: str, exit_str: str) -> Union[int, str]:
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        t1 = datetime.strptime(entry_str, fmt)
        t2 = datetime.strptime(exit_str, fmt)
    except ValueError:
        return "Invalid date format"
        
    diff = t2 - t1
    secs = diff.total_seconds()
    if secs < 0:
        return "Error: Exit time is before entry time"
        
    m = math.ceil(secs / 60)
    
    days = m // MINUTES_IN_DAY
    rem = m % MINUTES_IN_DAY
    
    cost = days * DAILY_CAP
    rem_cost = 0.0
    
    if rem <= FREE_MINUTES:
        rem_cost = 0
    elif rem <= HOURLY_RATE_1_LIMIT_MINUTES:
        rem_cost = rem * (HOURLY_RATE_1 / 60)
    else:
        rem_cost = HOURLY_RATE_1_LIMIT_MINUTES * (HOURLY_RATE_1 / 60) + (rem - HOURLY_RATE_1_LIMIT_MINUTES) * (HOURLY_RATE_2 / 60)
    
    rem_cost = min(rem_cost, DAILY_CAP)
    cost += rem_cost
    
    return round(cost)

def main() -> None:
    base_dir = Path(__file__).parent
    input_file = base_dir / "input.txt"
    if not input_file.exists():
        print("input.txt not found.")
        return
        
    lines = input_file.read_text(encoding="utf-8").strip().splitlines()
    if len(lines) < 2: 
        return
    
    txt_output_path = base_dir / "output.txt"
    csv_output_path = base_dir / "output.csv"
    
    results = []
    
    with open(txt_output_path, "w", encoding="utf-8") as f_txt:
        for line in lines[2:]:
            parts = [p.strip() for p in line.split("\t") if p.strip()]
            if len(parts) >= 3:
                plate = parts[0]
                entry = parts[1]
                exit_time = parts[2]
                res = calculate_fee(entry, exit_time)
                
                results.append({"Rendszam": plate, "Dij_Forint": res})
                
                out_line = f"{plate} -> {res} forint"
                print(out_line)
                f_txt.write(out_line + "\n")
                
    with open(csv_output_path, "w", encoding="utf-8", newline="") as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=["Rendszam", "Dij_Forint"])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()
