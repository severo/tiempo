# -*- coding: utf-8 -*-

""" produce a report from CSV time reporting files
"""

import argparse
import csv
import errno
import os

from collections import defaultdict
from collections import OrderedDict
from curses.ascii import isascii
from datetime import date
from datetime import datetime
from unicodedata import normalize

import matplotlib.pyplot as plt

def deaccentuate(t):
	return filter(isascii, normalize('NFD', t.decode('utf-8')).encode('utf-8').lower())

class MonthReport:
	def __init__(self):
		self.months = []
		self.reportedHours = []
		self.dueHours = []
		self.diffHours = []
		self.cumulHours = []

	def computeReportPerMonth(self, timeReports, keyword="", dueHoursTimeReports=None):
		od = timeReports.sumReportedTimePerMonth(keyword)

		self.months = od.keys()
		self.reportedHours = od.values()

		if dueHoursTimeReports:
			odh = dueHoursTimeReports.sumReportedTimePerMonth(keyword)

			# Extend both dictionnaries to cover the same months
			emptyod = { k: 0 for k in od.keys() }
			emptyodh = { k: 0 for k in odh.keys() }
			emptyod.update(odh)
			emptyodh.update(od)
			od = OrderedDict(sorted(emptyodh.items()))
			odh = OrderedDict(sorted(emptyod.items()))

			self.months = od.keys()
			self.reportedHours = od.values()
			self.dueHours = odh.values()
			self.diffHours = [self.reportedHours[i] - self.dueHours[i] for i in range(len(self.reportedHours))]
			self.cumulHours = [sum(self.diffHours[:i]) for i in range(1, len(self.diffHours)+1)]

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
					try:
						t = TimeReport()
						# first field should be a date (eg. 2013/11/20)
						t.date = datetime.strptime(row[0], '%Y/%m/%d').date()
						# second field should be a reported time (eg. 0.75)
						t.reportedTime = float(row[1])
						# third field should be a CSV list of keywords
						# (eg. "work,mail")
						t.keywords = deaccentuate(row[2]).split(",")
						# fourth field should be a description (eg. "reading")
						t.description = row[3]
						# Add to timeReports list
						self.add(t)
					except:
						print row

	def sortByDate(self):
		self.reports = sorted(self.reports, key=lambda r: r.date)

	def sortByReportedTime(self):
		self.reports = sorted(self.reports, key=lambda r: r.reportedTime)

	def sumReportedTime(self):
		return sum(r.reportedTime for r in self.reports)

	def sumReportedTimePerMonth(self, keyword=""):
		k = deaccentuate(keyword)
		d = defaultdict(float)
		for r in self.reports:
			if (len(k) == 0 or k in r.keywords):
				d[date(r.date.year,r.date.month,1)] += r.reportedTime
		od = OrderedDict(sorted(d.items()))
		return od

	def reportPerMonth(self, keyword="", dueHoursTimeReports=None):
		r = MonthReport()
		r.computeReportPerMonth(self, keyword, dueHoursTimeReports)

		s = "Reported time"
		if len(keyword):
			s += " for '" + keyword + "'"

		for i in range(len(r.months)):
			s += "\n* " + r.months[i].strftime("%b %Y") + ": " + str(r.reportedHours[i]) + " hours"
			if dueHoursTimeReports:
				s += ", due: " + str(r.dueHours[i]) + " hours, cumdiff: " + str(r.cumulHours[i])
		return s

	def graphPerMonth(self, keyword="", dueHoursTimeReports=None):
		r = MonthReport()
		r.computeReportPerMonth(self, keyword, dueHoursTimeReports)

		plt.plot(r.months, r.reportedHours, 'b-')
		if r.dueHours:
			plt.plot(r.months, r.dueHours, 'r-')
		if r.cumulHours:
			plt.plot(r.months, r.cumulHours, 'k--')
		plt.show()

parser = argparse.ArgumentParser(description='Analyze a time reporting CSV file.')
parser.add_argument('filepath', type=str, help='the file to analyze')
parser.add_argument('-k', '--keyword', metavar='keyword', default='', nargs='?', help='report only for this keyword')
parser.add_argument('-d', '--duehours', metavar='duehours', default='', nargs='?', help='csv file containing due hours in the same format than time reports')
args = parser.parse_args()

timeReports = TimeReports(args.filepath)

if (args.duehours):
	dueHours = TimeReports(args.duehours)
	print timeReports.reportPerMonth(args.keyword, dueHours)
	timeReports.graphPerMonth(args.keyword, dueHours)
else:
	print timeReports.reportPerMonth(args.keyword)
