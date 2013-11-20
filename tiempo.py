# -*- coding: utf-8 -*-

""" produce a report from CSV time reporting files
"""

import argparse

parser = argparse.ArgumentParser(description='Analyze a time reporting CSV file.')
parser.add_argument('file', type=str, help='the file to analyze')
parser.add_argument('-O', '--output', metavar='path', default='/tmp', nargs='?', type=str, help='output directory (default: %(default)s)')
args = parser.parse_args()
