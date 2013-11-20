# -*- coding: utf-8 -*-

""" produce a report from CSV time reporting files
"""

import argparse
import csv
from datetime import datetime
import errno
import os

class TimeReport:
	"""A time report correspond to one line in CSV file"""
	def __init__(self):
		self.date = None
		self.reportedTime = 0
		self.keywords = []
		self.description = ""

	def __str__(self):
		return "Date: " + str(self.date) + ", Reported Time: " + \
		       str(self.reportedTime) + ", Keywords: " + \
		       ', '.join(self.keywords) + ", Description: " + \
		       self.description

class TimeReports:
	def __init__(self, filepath=""):
		self.reports = []
		if len(filepath):
			self.appendCsvFile(filepath)

	"""Add a time report to list"""
	def add(self, t):
		self.reports.append(t)

	def __len__(self):
		return len(self.reports)

	def __str__(self):
		return '\n'.join(map(str, self.reports))

	def appendCsvFile(self, filepath):
		with open(filepath, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter='|')
			for row in reader:
				if len(row) == 4:
					t = TimeReport()
					# first field should be a date (eg. 2013/11/20)
					t.date = datetime.strptime(row[0], '%Y/%m/%d').date()
					# second field should be a reported time (eg. 0.75)
					t.reportedTime = float(row[1])
					# third field should be a CSV list of keywords
					# (eg. "work,mail")
					t.keywords = row[2].split(",")
					# fourth field should be a description (eg. "reading")
					t.description = row[3]
					# Add to timeReports list
					self.add(t)

	def sortByDate(self):
		self.reports = sorted(self.reports, key=lambda r: r.date)

	def sortByReportedTime(self):
		self.reports = sorted(self.reports, key=lambda r: r.reportedTime)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

parser = argparse.ArgumentParser(description='Analyze a time reporting CSV file.')
parser.add_argument('filepath', type=str, help='the file to analyze')
parser.add_argument('-O', '--output', metavar='path', default='/tmp', nargs='?', type=str, help='output directory (default: %(default)s)')
args = parser.parse_args()

outputdir = os.path.abspath(args.output)
resultbasename = os.path.basename(outputdir)

print "Analyzing " + args.filepath + ". Output in " + outputdir

mkdir_p(args.output)

timeReports = TimeReports(args.filepath)
print str(len(timeReports)) + " time reports"
timeReports.sortByDate()
print str(timeReports)
