def next_magic_num(s):
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

for case in ["808", "999", "2133", "1321", "9", "120"]:
    print(f"{case} -> {next_magic_num(case)}")
