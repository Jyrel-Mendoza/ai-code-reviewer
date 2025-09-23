# sample_test.py

import math


def badFunction(x, y):
    # adds two numbers in a very bad style
    return  x +   y


def unused_code():
    z = math.sqrt(16)
    # never used
    return


if __name__ == "__main__":
    print(badFunction(2,3))
