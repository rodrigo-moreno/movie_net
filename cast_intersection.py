from sys import argv
from movies import *

def cast_intersection(c1, c2):
    '''
    Gets the cast intersection of two movies defined by their codes.
    '''
    m1 = Movie(c1)
    m1.get_cast()
    m2 = Movie(c2)
    m2.get_cast()

    s1 = set(m1.cast)
    s2 = set(m2.cast)

    inter = s1 & s2
    return inter


if __name__ == '__main__':
    inter = cast_intersection(argv[1], argv[2])
    print(inter)

