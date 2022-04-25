import sys
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import math
import numpy as np
from geometry_functions import find_centroid, is_valid_position_in_circles, is_valid_position_in_squares


def create_mesh(nb_element, curvature, L, H, Xc, Yc, Rc, Xs, Ys, Sa, Sb):
    np.set_printoptions(threshold=sys.maxsize)
    nodes = np.empty(shape=[0, 2])

    dx = L / nb_element     #velikost facetu ve směru x
    dy = H / nb_element     #velikost facetu ve směru y

    #INICIALIZUJE TĚLO
    for x in np.linspace(0, L, nb_element):
        for y in np.linspace(0, L, nb_element):
            write = True

            for xc, yc, rc in zip(Xc, Yc, Rc):
                if not is_valid_position_in_circles(x, y, xc, yc, rc*1.05, empty=True):
                    write = False

            for xs, ys, sa, sb in zip(Xs, Ys, Sa, Sb):
                if not is_valid_position_in_squares(x, y, xs, ys, sa+dx/2, sb+dy/2):
                    write = False

            if write == True:
                nodes = np.append(nodes, [[x, y]], axis=0)

    #INICIALIZUJE CURVATURU KOLEM KRUHŮ
    for xc, yc, rc in zip(Xc, Yc, Rc):

        for i in range(curvature):

            x = xc + rc*math.cos(i * 2*math.pi * 1/curvature)
            y = yc + rc*math.sin(i * 2*math.pi * 1/curvature)
            if x >= 0 and x <= L and y >=0 and y <= L:
                nodes = np.append(nodes, [[x, y]], axis=0)

    #INICIALIZUJE NODY KOLEM ČTVERCŮ
    for xs, ys, sa, sb in zip(Xs, Ys, Sa, Sb):

        for x in np.arange(xs-sa, xs+sa+dx, dx):
            #vyřeší nody v rozích, které se netrefí do dx kvůli přestřelu
            if x > L and x < L+dx:
                x = L
            if x < 0 and x > 0 - dx:
                x = 0

            #vyřeší nody mimo doménu
            if x <= L+dx*0.1 and x > 0 and ys-sb > 0:
                nodes = np.append(nodes, [[x, ys-sb]], axis=0)
            if x <= L + dx*0.1 and x > 0 and ys + sb <= H:
                nodes = np.append(nodes, [[x, ys+sb]], axis=0)

        for y in np.arange(ys-sb, ys+sb+dy, dy):
            #vyřeší nody v rozích, které se netrefí do dy
            if y > H and y < H + dy:
                y = H
            if y < 0 and y > 0 - dy:
                y = 0

            if y <= H+dy*0.1 and y > 0 and xs-sa > 0 :
                nodes = np.append(nodes, [[xs-sa, y]], axis=0)
            if y <= H+dy*0.1 and y > 0 and xs + sa < L:
                nodes = np.append(nodes, [[xs+sa, y]], axis=0)


    tri = Delaunay(nodes)
    mesh = np.array(tri.simplices)
    facet_nodes = nodes[tri.simplices]
    print(np.shape(facet_nodes))

    final_mesh = []

    #VYMAZAT FACETY, KTERÉ SE NACHÁZÍ V ZAKÁZANÝCH OBLASTECH
    for i in range(len(facet_nodes)):
        Tx = find_centroid(facet_nodes, i)[0]
        Ty = find_centroid(facet_nodes, i)[1]

        write = True
        for xc, yc, rc in zip(Xc, Yc, Rc):
            if not is_valid_position_in_circles(Tx, Ty, xc, yc, rc, empty=True):
                write = False

        for xs, ys, sa, sb in zip(Xs, Ys, Sa, Sb):
            if not is_valid_position_in_squares(Tx, Ty, xs, ys, sa, sb):
                write = False

        if Tx > L or Tx < 0:
            write = False
        if Ty > H or Ty < 0:
            write = False

        if write == False:
            print("deleting node #", i)

        else:
            row = []
            for j in range(3):
                row.append(mesh[i][j])
            final_mesh.append(row)

    #PLOT MESH
    plt.triplot(nodes[:, 0], nodes[:, 1], final_mesh)
    plt.gca().set_aspect('equal')
    plt.plot(nodes[:,0], nodes[:,1], 'o')
    plt.show()





