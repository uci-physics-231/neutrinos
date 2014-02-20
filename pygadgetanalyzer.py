#!/usr/bin/env python
"""
Does stuff.
"""
import argparse
import numpy as np
import pynbody
import sys
from matplotlib import pyplot as plt

def plot(argv):
    """
    Parses command line arguments for function plot().
    Plots things.
    """
    parser = argparse.ArgumentParser(description="Plots a GADGET snapshot file.")
    parser.add_argument('infile', help="snapshot file name")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-f", "--family", help="specify family of particle to plot from {gas, dm, star}", \
            choices=['g', 'gas', 'd', 'dm', 's', 'star'], default='dm')
    parser.add_argument("-p", "--profile", help="specify profile type, e.g. density, mass, etc.", \
            choices=['density','mass','n'], default='density')
    parser.add_argument("--xscale", help="choose between log or linear x axis", choices=['log','linear'], \
            default='log')
    parser.add_argument("--yscale", help="choose between log or linear y axis", choices=['log','linear'], \
            default='log')
    parser.add_argument("--xlabel", help="label for x axis", default="x axis")
    parser.add_argument("--ylabel", help="label for y axis", default="y axis")
    parser.add_argument("--dim", help="spatial dimensions", type=int, choices=[2,3], default=2)
    args = parser.parse_args(argv)

    # Prep data for plotting
    snapshot = pynbody.load(args.infile)
    halos = snapshot.halos()
    pynbody.analysis.angmom.faceon(halos[1])
    snapshot.physical_units()
    prof = pynbody.analysis.profile.Profile(getattr(halos[1],args.family),min=.01,max=50,ndim=args.dim)

    # Make plot
    plt.plot(prof['rbins'],prof['density'])
    plt.xscale(args.xscale)
    plt.yscale(args.yscale)
    plt.xlabel(r'$%s$' % args.xlabel.replace('#','\\'))
    plt.ylabel(r'$%s$' % args.ylabel.replace('#','\\'))
    plt.show()

def print_help(argv):
    print "Usage:"
    print "    ./pygadgetanalyzer <command> [<args>]"
    print ""
    print "Available commands:"
    print "    %-12s Prints this help message" % "help"
    print "    %-12s Calculates quantities from a GADGET snapshot file" % "calc"
    print "    %-12s Plots a GADGET snapshot file" % "plot"
    print ""
    print "Type './pygadgetanalyzer.py <command> --help' for help regarding a command."


actions = {
        'help': print_help,
        'plot': plot,
        }

if __name__ == "__main__":
#    actions[sys.argv[1]](sys.argv[2:])
    try:
        actions[sys.argv[1]](sys.argv[2:])
    except:
        print "There was an error."
        print_help()
