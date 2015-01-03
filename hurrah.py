import pygame
import sys
import json
from datetime import datetime
pygame.init()

SECONDSINHOUR = 3600
SECONDSINDAY = SECONDSINHOUR * 24
SECONDSINWEEK = SECONDSINDAY * 7
MINYEAR = 2000

def sortListByItemIndex(_list, index):
	innerValueList = []
	sortedList = []
	for item in _list:
		innerValueList.append(item[index])
	innerValueList = sorted(innerValueList)
	for value in innerValueList:
		for item in _list:
			if item[index] == value:
				sortedList.append(item)
	return sortedList
def sortObjectsByAttribute(_list, attribute): ##Attribute should be given as a string
	attributeList = []
	sortedList = []
	for item in _list:
		attributeList.append(getattr(item, attribute))
	attributeList = sorted(attributeList)
	for attributeValue in attributeList:
		for item in _list:
			if getattr(item, attribute) == attributeValue:
				sortedList.append(item)
	return sortedList


class Data: ##Datum class (inside) takes a dictionary with time, value, and type
	def add():
		dataToAdd = []
		for datum in storedValues:
			datumDict = {"Time": datum.time, "Value": datum.value, "Type": datum.type}
			dataToAdd.append(datumDict)		
		database = "Blood Sugar Data.txt"
		databaseObject = open(database, "w")
		json.dump(dataToAdd, databaseObject)
		databaseObject.close()
	def update():
		database = "Blood Sugar Data.txt"
		databaseObject = open(database, "r")
		dataDict = json.load(databaseObject)
		storedValues = []
		i = 0
		for datum in dataDict:
			datum = Data.Datum(datum)
			print(datum.time)
			storedValues.append(datum)
		storedValues = sortObjectsByAttribute(storedValues, "time")
		databaseObject.close()
		return storedValues

	class Datum():
		def __init__(self, dictionary):
			self.time = int(dictionary["Time"])
			self.value = int(dictionary["Value"])

def yearIsLeapYear(year):
	if (year - MINYEAR) % 4 == 0:
		return True
	else:
		return False

def convertStupidDateIntToDatetimeObject(stupidDateInt):
	stupidDateInt = str(stupidDateInt)
	print(stupidDateInt)
	newDate = datetime(int(stupidDateInt[0] + stupidDateInt[1] + stupidDateInt[2] + stupidDateInt[3]), int(stupidDateInt[4] + stupidDateInt[5]), int(stupidDateInt[6] + stupidDateInt[7]), int(stupidDateInt[8] + stupidDateInt[9]), int(stupidDateInt[10] + stupidDateInt[11]))
	return newDate

def convertDateToSecondsSinceY2K(datetimeObj): ##Conversion is from datetime object.
	def secondsInYearsSinceY2K(datetimeObj):
		SECONDSINLEAPYEAR = 366 * SECONDSINDAY
		SECONDSINNORMALYEAR = 365 * SECONDSINDAY

		secondsInYearsSinceY2K = 0
		leapYearsSinceY2K = []
		normalYearsSinceY2K = []

		workingYear = datetimeObj.year
		while workingYear > MINYEAR:
			if yearIsLeapYear(workingYear):
				leapYearsSinceY2K.append(workingYear)
			else:
				normalYearsSinceY2K.append(workingYear)
			workingYear -= 1

		datetimeObj.year - MINYEAR

		for year in leapYearsSinceY2K:
			secondsInYearsSinceY2K += SECONDSINLEAPYEAR
		for year in normalYearsSinceY2K:
			secondsInYearsSinceY2K += SECONDSINNORMALYEAR

		return secondsInYearsSinceY2K

	def secondsPassedSinceNewYear(datetimeObj):
		monthsInLastYear = []
		daysPassedSinceNewYear = 0

		for month in range(1, 12): ##Gets a list of months excluding current month
			if month < datetimeObj.month:
				monthsInLastYear.append(month)

		for month in monthsInLastYear: ##Adds seconds in each month passed total
			if month in set([1, 3, 5, 7, 8, 10, 12]):
				daysPassedSinceNewYear += 31
			if month in set([4, 6, 9, 11]):
				daysPassedSinceNewYear += 30
			if month == 2:
				if yearIsLeapYear(datetimeObj.year):
					daysPassedSinceNewYear += 29
				else:
					daysPassedSinceNewYear += 28

		secondsInLastMonth = datetimeObj.day * SECONDSINDAY
		secondsInLastDay = (datetimeObj.hour * SECONDSINHOUR) + (datetimeObj.minute * 60)
		secondsPassedSinceNewYear = (daysPassedSinceNewYear * SECONDSINDAY) + secondsInLastMonth + secondsInLastDay
		return secondsPassedSinceNewYear

	secondsSinceY2K = secondsInYearsSinceY2K(datetimeObj) + secondsPassedSinceNewYear(datetimeObj)
	return secondsSinceY2K

storedValues = Data.update()
for datum in storedValues:
	datum.time = convertStupidDateIntToDatetimeObject(datum.time)
	datum.time = convertDateToSecondsSinceY2K(datum.time)

Data.add()