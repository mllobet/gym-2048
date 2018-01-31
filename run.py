#! /usr/bin/env python3

import sys
import copy
from Game import Game

if __name__ == "__main__":
    g = Game(4)
    print(g)
    for line in sys.stdin:
        if line == 'w\n':
            line = 0
        elif line == 'a\n':
            line = 3
        elif line == 'd\n':
            line = 1
        else:
            line = 2
        g.move(line)
        print(g)

