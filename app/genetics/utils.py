

def position_2_string(state):
    rows = ["8", "8", "8", "8", "8", "8", "8", "8"]
    for col, row in enumerate(state):
        if col in (0, 1, 2, 3, 4, 5, 6, 7):
            rem = int(rows[row-1][-1])
            before = str(rem - (8 - col)) if rem - (8 - col) != 0 else ""
            after = str(8 - (col + 1)) if 8 - (col + 1) > 0 else ""
            rows[row-1] = rows[row-1][:-1] + before + "Q" + after
        
    rows.reverse()
    return "/".join(rows)