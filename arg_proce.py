
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
    example_text = '''Examples:

1. Only input file is required. (By default, the Pareto-preferred answer sets will be returned.)
  $ python lpod2asprin.py -i Examples/hotel.txt

2. You can also assign the preference type to one of {c, i, p, ps}.
  $ python lpod2asprin.py -i Examples/hotel.txt -type c

3. You can pass some options to asprin solver with [-a "OPTIONS"]. If the option is a single constant assignment such as "-c n=3", you can directly put it as an option.
  $ python lpod2asprin.py -i Examples/N_abc.txt -type c -a "-c n=3"
  $ python lpod2asprin.py -i Examples/N_abc.txt -type c -sc n=3'''

    parser = argparse.ArgumentParser(description='LPOD2ASPRIN: an LPOD solver using asprin', epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', help='input file. [REQUIRED]', nargs=1, required=True)
    parser.add_argument('-type', help='lpod preference type, by default is p', nargs=1)
    parser.add_argument('-sc', help='define single constant', nargs=1)
    parser.add_argument('-a', help='asprin options passed as it is to the solver. Pass all asprin options in \"double quotes\"', nargs=1)

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

    if args.sc is not None:
        arglist.append("-constant "+args.sc[0])

    if args.a is not None:
        arglist.append("-asprin "+args.a[0].strip("\""))


    return arglist