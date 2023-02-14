from cols import COLS

def row(data, t):
    if data.cols:
        data.rows.append(t)
        for cols in [data.cols.x, data.cols.y]:
            for col in cols:
                add(col, t[col.at])
    else:
        data.cols = COLS(t)
    return data
