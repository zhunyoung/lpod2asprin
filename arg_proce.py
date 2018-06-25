
# !/usr/bin/python
import argparse
import sys
import os
from math import exp
from subprocess import Popen, PIPE


def print_error(error, dest):
    if error is not None:
        if dest is not None:
            print_output(error, dest)
        else:
            print (sys.stderr, "*** Error \n")
            print ( sys.stderr, error)


def processOutput(output, mf):
    val = 0
    for line in output.split("\n"):
        if "Optimization:" in line:
            val = val + exp(-1 * (int(line.split()[-1]) / 1000.0))
    return val


def main():
    parser = argparse.ArgumentParser(description='LPOD2ASPRIN')
    parser.add_argument('-i', help='input file. [REQUIRED]', nargs=1)
    parser.add_argument('-type', help='lpod preference type, by default is p', nargs=1)

    args = parser.parse_args()

    arglist = []
    if args.i is None or not os.path.isfile(args.i[0]):
        print_error("Check input file.", None)
        parser.print_help()
        sys.exit(0)
    else:
        arglist.append(args.i[0])


    if args.type is not None:
        arglist.append("-c lpodPrefType="+args.type[0])
    else:
        arglist.append("-c lpodPrefType=p")


    return arglist