import math
from datetime import datetime

def calculate_fee(entry_str, exit_str):
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
    
    days = m // 1440
    rem = m % 1440
    
    cost = days * 10000
    if rem <= 30:
        rem_cost = 0
    elif rem <= 180:
        rem_cost = rem * 5
    else:
        rem_cost = 180 * 5 + (rem - 180) * (500 / 60)
    
    rem_cost = min(rem_cost, 10000)
    cost += rem_cost
    
    return round(cost)

print("ABC-123:", calculate_fee("2026-03-30 07:45:12", "2026-03-30 09:10:33")) # ~85 mins
print("Error case:", calculate_fee("2026-03-30 09:10:33", "2026-03-30 07:45:12"))
print("30 hours:", calculate_fee("2026-03-30 00:00:00", "2026-03-31 06:00:00")) # 30 hours = 1 day + 6 hours = 10000 + 1400 = 11400
