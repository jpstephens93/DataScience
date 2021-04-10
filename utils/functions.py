def coordinates_range(x, y=None, step=1):
    if y is None:
        return range(x)
    else:
        coord = [x]
        i = coord[0]
        while i <= (y - step):
            i += step
            i = round(i, 2)
            coord.append(i)
        return coord
