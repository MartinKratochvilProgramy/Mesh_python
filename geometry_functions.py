def find_centroid(facet_points, i):
    Tx = 0
    Ty = 0
    for j in range(3):
        Tx += facet_points[i][j][0]
        Ty += facet_points[i][j][1]

    Tx = Tx/3
    Ty = Ty/3

    return Tx, Ty

def is_valid_position_in_circles(x, y, xc, yc, rc, empty=True):
    if empty == True:
        if (x-xc)**2 + (y-yc)**2 <= rc**2:
            return False
        else:
            return True
    elif empty == False:
        if (x-xc)**2 + (y-yc)**2 >= rc**2:
            return False
        else:
            return True

def is_valid_position_in_squares(x, y, xs, ys, sa, sb, empty=True):
    if empty == True:
        if (xs-sa) < x <(xs+sa) and (ys-sb) < y < (ys+sb):
            return False
        else:
            return True