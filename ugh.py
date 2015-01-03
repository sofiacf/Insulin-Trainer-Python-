from datetime import datetime

SECONDSINHOUR = 3600
SECONDSINDAY = SECONDSINHOUR * 24
SECONDSINWEEK = SECONDSINDAY * 7
MINYEAR = 2000

dates = [201412032220, 201412032220, 201412051247, 201412051320, 201412051936, 201412061445, 201412071302, 201412091316, 201412092300, 201412272041, 201412280251, 201412280940, 201412281322, 201412281934]

def yearIsLeapYear(year):
	if (year - MINYEAR) % 4 == 0:
		return True
	else:
		return False

def convertStupidDateIntsToDatetimeObjects(dates):
	newDates = []
	for date in dates:
		date = str(date)
		date = datetime(int(date[0] + date[1] + date[2] + date[3]), int(date[4] + date[5]), int(date[6] + date[7]), int(date[8] + date[9]), int(date[10] + date[11]))
		newDates.append(date)
	return newDates

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
			elif month == set([4, 6, 9, 11]):
				daysPassedSinceNewYear += 30
			elif month == 2:
				if yearIsLeapYear(datetimeObj.year):
					daysPassedSinceNewYear += 29
				else:
					daysPassedSinceNewYear += 28

		secondsThisMonth = datetimeObj.day * SECONDSINDAY
		secondsInLastDay = (datetimeObj.hour * SECONDSINHOUR) + (datetimeObj.minute * 60)
		secondsPassedSinceNewYear = (daysPassedSinceNewYear * SECONDSINDAY) + secondsThisMonth + secondsInLastDay
		return secondsPassedSinceNewYear

	secondsSinceY2K = secondsInYearsSinceY2K(datetimeObj) + secondsPassedSinceNewYear(datetimeObj)
	return secondsSinceY2K


dates = convertStupidDateIntsToDatetimeObjects(dates)
newDates = []
for date in dates:
	date = convertDateToSecondsSinceY2K(date)
	newDates.append(date)
dates = newDates
print("                          ", dates)