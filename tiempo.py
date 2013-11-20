# -*- coding: utf-8 -*-

""" produce a report from CSV time reporting files
"""

import argparse
import errno
import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

parser = argparse.ArgumentParser(description='Analyze a time reporting CSV file.')
parser.add_argument('file', type=str, help='the file to analyze')
parser.add_argument('-O', '--output', metavar='path', default='/tmp', nargs='?', type=str, help='output directory (default: %(default)s)')
args = parser.parse_args()

outputdir = os.path.abspath(args.output)
resultbasename = os.path.basename(outputdir)

print "Analyzing " + args.file + ". Output in " + outputdir

mkdir_p(args.output)
