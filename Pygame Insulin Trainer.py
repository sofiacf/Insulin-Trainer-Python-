import pygame
import sys
import json
from datetime import datetime
pygame.init()
def Setup():
	global width, height, screen, key, aValueHasBeenSubmittedRecently
	global numbers, currentNumber, inputNumbers, storedValues
	(width, height) = (500, 500)
	screen = pygame.display.set_mode((width, height))
	key = pygame.key.get_pressed()
	pygame.display.set_caption("Insulin Trainer")
	try:
		storedValues = Data.update()
	except ValueError:
		storedValues = []
	aValueHasBeenSubmittedRecently = False
	class Number():
		def __init__(self, value):
			self.image = pygame.image.load("%s.png" %value)
			self.value = value
		def setupNumbers():
			numbers = []
			for number in range(10):
				numbers.append(Number(number))
			return numbers
	numbers = Number.setupNumbers()
	currentNumber = ""
	inputNumbers = []
class Data():
	def add():
		dataToAdd = []
		for datum in storedValues:
			datumDict = {"Time": datum.time, "Value": datum.value, "Type": datum.type}
			dataToAdd.append(datumDict)
		inputFile = "Blood Sugar Data.txt"
		inputFileObject = open(inputFile, 'w')
		json.dump(dataToAdd, inputFileObject)
		inputFileObject.close()
	def update():
		inputFile = "Blood Sugar Data.txt"
		inputFileObject = open(inputFile, 'r')
		dataDictionary = json.load(inputFileObject)
		storedValues = []
		for datum in dataDictionary:
			datum = Data.Datum(datum)
			storedValues.append(datum)
		inputFileObject.close()
		return storedValues
	class Datum():
		def __init__(self, dictionary):
			self.time = int(dictionary["Time"])
			self.value = int(dictionary["Value"])
			self.type = dictionary["Type"]
Setup()
class Button(): ##Other control buttons
	def __init__(self, image, isSelected, commonName, position):
		self.image = pygame.image.load(image)
		self.selected = isSelected
		self.name = commonName
		self.size = pygame.Surface.get_size(self.image)
		self.pos = position
def ButtonSetup():
	global cancel, add
	cancel = Button("cancel.png", False, "cancel", 100)
	cancel.pos = (width - cancel.size[0], 100)
	add = Button("add.png", False, "add", 85)
	add.pos = (width - add.size[0], 85)
ButtonSetup()
class AddMenu(Button): ##Buttons to display input fields
	def __init__(self, image, inputID, isSelected, commonName, field, displayed):
		self.image = pygame.image.load(image)
		self.id = inputID
		self.selected = isSelected
		self.name = commonName
		self.pos = (width - pygame.Surface.get_size(self.image)[0], pygame.Surface.get_size(self.image)[1] * self.id)
		self.size = pygame.Surface.get_size(self.image)
		self.field = field
		self.fieldpos = (width - pygame.Surface.get_size(self.field)[0], 0)
		self.displayed = displayed
def AddMenuSetup():
	global bloodSugarButton, insulinDoseButton, foodConsumptionButton, MenuButtons, allTheButtons
	bloodSugarButton = AddMenu("Blood Sugar Button.png", 0, False, "Blood Sugar", pygame.image.load("Blood Sugar Input Field.png"), False)
	insulinDoseButton = AddMenu("Insulin Dose Button.png", 1, False, "Insulin Dose", pygame.image.load("Insulin Dose Input Field.png"), False)
	foodConsumptionButton = AddMenu("Food Consumption Button.png", 2, False, "Food Consumption", pygame.image.load("Food Consumption Input Field.png"), False)
	MenuButtons = [bloodSugarButton, foodConsumptionButton, insulinDoseButton]
AddMenuSetup()
class Graph():
	def __init__(self, width, height, position, color):
		self.width = width
		self.height = height
		self.size = (self.width, self.height)
		self.position = position
		self.color = color
		self.Surface = pygame.Surface(self.size)
		self.myrange = Graph.Range('month', 201412010000)
	class Range():
		global unitConversion
		unitConversion = {'year': 12000000, 'month': 310000, 'day': 2400, 'hour': 60}
		def __init__(self, unit, start, points=[]):	
			self.unit = unit
			self.convertedunit = unitConversion[unit]
			self.start = start
			self.points = points
	def graphControl(self):
		global placeHolderRangeButton, rangeHasRecentlyBeenChanged, rightArrow, leftArrow
		class RangeButton():
			def __init__(self, image, rangeattributematcher, isSelected = False):
				self.image = pygame.image.load("%s" % image)
				self.size = pygame.Surface.get_size(self.image)
				self.width = self.size[0]
				self.height = self.size[1]
				self.rangeattributematcher = rangeattributematcher
				self.xpos = (width / 2) - (self.width / 2) ##Center of the screen on x axis
				self.ypos = 50 - self.height
				self.pos = (self.xpos, self.ypos)
				self.selected = isSelected
		hour = RangeButton("Hour.png", 'hour')
		day = RangeButton("Day.png", 'day')
		month = RangeButton("Month.png", 'month')
		rangeButtons = [hour, day, month]
		leftArrow = RangeButton("LeftArrow.png", -1)
		rightArrow = RangeButton("RightArrow.png", 1)
		navigationButtons = [leftArrow, rightArrow]
		try:
			placeHolderRangeButton
		except NameError:
			placeHolderRangeButton = RangeButton("Hour.png", 'hour') ##For isSelected
		leftArrow.pos = (placeHolderRangeButton.xpos - leftArrow.width, placeHolderRangeButton.ypos)
		rightArrow.pos = (placeHolderRangeButton.xpos + placeHolderRangeButton.width, placeHolderRangeButton.ypos)
		def displayRangeControl():
			for button in rangeButtons:
				if self.myrange.unit == button.rangeattributematcher:
					screen.blit(button.image, (button.pos))
			for button in navigationButtons:
				screen.blit(button.image, button.pos)
		def setRangeUnit():
			possibleUnits = ['hour', 'day', 'month']; i = 0
			for possibleunit in possibleUnits:
				if self.myrange.unit == possibleunit:
					if i < len(possibleUnits) - 1:
						self.myrange.unit = possibleUnits[i + 1]
						self.myrange.convertedunit = unitConversion[self.myrange.unit]
					else:
						self.myrange.unit = possibleUnits[0]
						self.myrange.convertedunit = unitConversion[self.myrange.unit]
				else: i += 1
		def modifyRangeStart():
			modificationIncrements = {'hour': 100, 'day': 10000, 'month': 1000000, 'year': 100000000}
			for button in navigationButtons:
				if button.selected:
					for unit in modificationIncrements:
						if self.myrange.unit == unit:
							self.myrange.start += (unit*button.rangeattributematcher)
							button.self = False
		displayRangeControl()
		modifyRangeStart()
		if placeHolderRangeButton.selected == True and rangeHasRecentlyBeenChanged == False:
			rangeHasRecentlyBeenChanged = True
			setRangeUnit()
			placeHolderRangeButton.selected = False
	def displayGraph(self): ##Blits a graph, and does a shit ton of stuff with ranges and points lulz
		screen.blit(self.Surface, self.position)
		self.Surface.fill(self.color)
		def getPointsInRange(): ##Sets points attribute for a range object
			self.myrange.points = []
			for datum in storedValues:
				if self.myrange.start < datum.time < self.myrange.start + self.myrange.convertedunit:
					self.myrange.points.append(datum)
		def convertValueToPosition(): ##Returns list of dicts points as w/ type and pos
			heightConverter = 1.6
			posPointDivisor = self.myrange.convertedunit / self.width
			xmax = self.myrange.start + self.myrange.convertedunit
			for datum in self.myrange.points:
				xpos = self.width - int((((xmax - datum.time) / self.myrange.convertedunit) * self.width))
				if datum.type == "Blood Sugar":
					ypos = self.height - int(datum.value * heightConverter)
				else:
					ypos = (50)
				datum.position = (xpos, ypos)
		inputSymbols = {"Blood Sugar": pygame.image.load("Blood Sugar Point.png"), "Insulin Dose" : pygame.image.load("Insulin Dose Point.png"), "Food Consumption": pygame.image.load("Food Consumption Point.png")}
		pointCenterCorrector = (pygame.Surface.get_size(pygame.image.load("Blood Sugar Point.png"))[0]/2)
		def plotPoints(): ##Blits points from pointsToGraph, pos corrected to center; draws connecting lines
			lineDrawingList = []
			for datum in self.myrange.points:
				if datum.type == "Blood Sugar":
					lineDrawingList.append(datum.position)
			lineDrawingList = (sorted(lineDrawingList))
			pygame.draw.aalines(self.Surface, (250, 0, 0), False, lineDrawingList)
			for datum in self.myrange.points:
				if datum.type == "Blood Sugar":
					self.Surface.blit(inputSymbols["Blood Sugar"], ((datum.position[0] - pointCenterCorrector), datum.position[1] - pointCenterCorrector))
		getPointsInRange()
		convertValueToPosition()
		try: plotPoints()
		except: ValueError
myGraph = Graph(width - 100, height - 100, (50, 50), (0, 0, 0))
myGraph.graphControl()
allTheButtons = [bloodSugarButton, foodConsumptionButton, insulinDoseButton,
					add, cancel, placeHolderRangeButton, rightArrow, leftArrow]
def displayInput():
	if displayInputWindow() and len(inputNumbers) > 0:
		for number in numbers:
			for inputnumber in inputNumbers:
				if str(number.value) == inputNumber[0]:
					screen.blit(number.image, (len(inputNumbers) * 10, 0))
def displayMenuButtons(): ##Blits the usual menu buttons.
	for button in MenuButtons:
		screen.blit(button.image, button.pos)		 
def isButtonPressed():
	global aValueHasBeenSubmittedRecently, rangeHasRecentlyBeenChanged
	if pygame.mouse.get_pressed()[0] == True:
		for button in allTheButtons:
			inX = False
			inY = False
			if button.pos[0] <= pygame.mouse.get_pos()[0] <= button.pos[0] + button.size[0]:
				inX = True
			if button.pos[1] <= pygame.mouse.get_pos()[1] <= button.pos[1] + button.size[1]:
				inY = True
			if inX and inY:
				button.selected = True
				print(button.pos, button.size, button, leftArrow.pos, leftArrow.size, leftArrow)
			else: button.selected = False
			if add.selected == True and aValueHasBeenSubmittedRecently == False:
				submit()
				aValueHasBeenSubmittedRecently = True
				add.selected = False
	else: aValueHasBeenSubmittedRecently = False; rangeHasRecentlyBeenChanged = False
def displayInputWindow(): ##Shows the input screen until cancel.
	global currentNumber, inputNumbers
	for button in MenuButtons:
		if button.selected == True and cancel.selected == False:
			screen.blit(button.field, button.fieldpos)
			screen.blit(cancel.image, cancel.pos)
			screen.blit(add.image, add.pos)
			button.displayed = True
			return True
		elif cancel.selected == True or add.selected == True:
			button.selected = False
			currentNumber = []
			inputNumbers = []
			return False
def collectInput(event): ##Adds numbers to inputNumbers; calls submit
	global inputNumbers
	if displayInputWindow():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				if len(inputNumbers) != 0:
					inputNumbers.pop()
			elif event.key == pygame.K_RETURN:
				submit()
				inputNumbers = []
			elif int(event.unicode) in range(10) and len(inputNumbers) < 3:
				inputNumbers.append([event.unicode, (len(inputNumbers)*10, 0)])
			else:
				print("That is not acceptable input. Please try again with a /NUMBER/.")
def displayInput(): ##Blits numbers as user types
	if displayInputWindow() and len(inputNumbers) > 0:  
		for number in numbers:
			for inputNumber in inputNumbers:
				if str(number.value) == inputNumber[0]:
					screen.blit(number.image, inputNumber[1])
def submit(): ##Creates storedValues dict and calls Data.add()  it
	global storedValues, currentNumber
	def getCurrentNumber(): ##Strips position from inputNumbers
		currentNumber = ""
		if len(currentNumber) < len(inputNumbers):
			for inputnumber in inputNumbers:
				currentNumber = currentNumber + inputnumber[0]
		if len(currentNumber) >= 1:
			currentNumber = str(currentNumber)
		return str(currentNumber)
	currentNumber = getCurrentNumber()
	def getCurrentTime():
		currentTime = ""
		now = datetime.now()
		dateAttributes = [now.year, now.month, now.day, now.hour, now.minute]
		for attribute in dateAttributes:
			if len(str(attribute)) < 2:
				attribute = "0%s" % str(attribute)
			currentTime = currentTime + str(attribute)
		return currentTime
	currentTime = getCurrentTime()
	def getInputType():
			for button in MenuButtons:
				if button.displayed == True:
					Type = button.name
			return Type
	Type = getInputType()
	add.selected = True
	if len(currentNumber) != 0:
		newDatum = {"Value": currentNumber, "Time": currentTime, "Type": Type}
		storedValues.append(Data.Datum(newDatum))
	Data.add()
clock = pygame.time.Clock()
running = True
while running:
	key = pygame.key.get_pressed()
	pygame.Surface.fill(screen, (0x445566))
	myGraph.displayGraph()
	myGraph.graphControl()
	displayMenuButtons()
	isButtonPressed()
	displayInputWindow()
	displayInput()
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		else:
			collectInput(event)
	clock.tick(20)
sys.exit()