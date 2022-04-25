import numpy as np
L = 1
H = 1
#definice prázdných kružnic
Xc = np.array([0., 0.5])
Yc = np.array([0., 0.5])
Rc = np.array([0.1, 0.2])

#definice prázdných obdélníků - středy
Xs = np.array([1])
Ys = np.array([1])
#definice prázdných obdélníků - šířka směr a=x, výška směr b=y
Sa = np.array([0.18])
Sb = np.array([0.18])

nb_element = 20     #počet elementů v každém směru
curvature = 20      #počet elementů po obvodu kružnic


