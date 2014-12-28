import pygame
import sys
import json
from datetime import datetime
pygame.init()
def Setup():
	global SCREENWIDTH, SCREENHEIGHT, screen,  black, red
	global storedValues, clock, running, today, buttons
	global currentInputCollector, currentWindow, inputNumbers

	running = True
	currentInputCollector = False
	currentWindow = False
	inputNumbers = []
	black = (0, 0, 0); red = (230, 0, 0)

	(SCREENWIDTH, SCREENHEIGHT) = (500, 500)
	screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
	pygame.display.set_caption("Insulin Trainer")
	
	clock = pygame.time.Clock()
	
	def getTodaysDate():
		today = ""
		now = datetime.now()
		dateUnits = [now.year, now.month, now.day]
		for unit in dateUnits:
			unit = str(unit)
			if len(unit) < 2:
				unit = "0%s" % unit
			today = today + unit
		return int(today+"0000")
	today = getTodaysDate()
	buttons = []

	try:
		storedValues = Data.update()
	except ValueError:
		storedValues = []

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
		for datum in dataDict:
			datum = Data.Datum(datum)
			storedValues.append(datum)
		databaseObject.close()
		return storedValues

	class Datum():
		def __init__(self, dictionary):
			self.time = int(dictionary["Time"])
			self.value = int(dictionary["Value"])
			self.type = dictionary["Type"]

Setup()

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
def sortObjectsByAttribute(_list, attribute):
	attributeList = []
	sortedList = []
	for item in _list:
		attributeList.append(item.attribute)
	attributeList = sorted(attributeList)
	for attributeValue in attributeList:
		for item in _list:
			if item.attribute == attributeValue:
				sortedList.append(item)
	return sortedList	

class Graph(): ##Takes width, height, pos, menu, optional timeRange
	class Point(Data.Datum): ##takes time, value, type
		def __init__(self, time, value, _type):
			self.time = time
			self.value = value
			self.type = _type
			self.image = pygame.image.load(self.type + " Point.png")
			self.size = pygame.Surface.get_size(self.image)
			start = 0
			self.pos = (start, start)
	class Range():
		def __init__(self, unit, start, points=[]):
			unitVals = {"year": 12000000, "month": 310000, "day": 2400, "hour": 60}
			self.unit = unit
			self.unitVal = unitVals[unit]
			self.start = start
			self.cutoff = start + self.unitVal
			self.points = []
		def changeUnit(button):
			unitVals = {"year": 12000000, "month": 310000, "day": 2400, "hour": 60}
			graph.timeRange.unit = button.name
			graph.timeRange.unitVal = unitVals[button.name]
		def changeStart(button):
			if button == leftArrow:
				direction = -1
			else:
				direction = 1
			graph.timeRange.start += graph.timeRange.unitVal*direction

	def __init__(self, width, height, position, menu, timeRange=Range("day", today)):
		self.width = width
		self.height = height
		self.pos = position
		self.menu = menu
		self.color = black
		self.surface = pygame.Surface((width, height))
		self.timeRange = timeRange
	
	def getPoints(self):
		for datum in storedValues:
			if self.timeRange.start < datum.time < self.timeRange.cutoff:
				newPoint = Graph.Point(datum.time, datum.value, datum.type)
				self.timeRange.points.append(newPoint)
	def setPointPositions(self):
		heightMultiplier = 1.6
		domainDivisor = self.timeRange.unitVal / self.width
		xmax = graph.timeRange.cutoff
		for point in self.timeRange.points:
			xpos = self.width - int(self.width * (xmax - point.time) / self.timeRange.unitVal)
			if point.type == "Blood Sugar":
				ypos = graph.height - int(point.value * heightMultiplier)
			else:
				ypos = graph.height
			point.pos = (xpos, ypos)
	def drawLines(self):
		lineDrawingList = []
		for point in self.timeRange.points:
			if point.type == "Blood Sugar":
				lineDrawingList.append(point.pos)
		lineDrawingList = sortListByItemIndex(lineDrawingList, 0)
		if len(lineDrawingList) > 1:
			pygame.draw.aalines(self.surface, red, False, lineDrawingList)
	def plotPoints(self):
		for point in self.timeRange.points:
			correctedPosition = (point.pos[0] - point.size[0]/2, point.pos[1] - (point.size[1]/2))
			self.surface.blit(point.image, correctedPosition)
	
	def displayGraph(self):
		screen.blit(self.surface, self.pos)
		self.getPoints()
		self.setPointPositions()
		self.drawLines()
		self.plotPoints()

class Button(): ##Takes image, name, opt selection, opt position, and opt action
	def __init__(self, image, name, isSelected=False, position=(0,0), action=None):
		global buttons
		self.image = pygame.image.load(image)
		self.name = name
		self.selected = isSelected
		self.size = pygame.Surface.get_size(self.image)
		self.pos = position
		self.xbounds = (position[0], position[0] + self.size[0])
		self.ybounds = (position[1], position[1] + self.size[1])
		self.action = action
		buttons.append(self)
	def updateBounds(self):
		self.xbounds = (self.pos[0], self.pos[0] + self.size[0])
		self.ybounds = (self.pos[1], self.pos[1] + self.size[1])

class InputCollector(): ##Takes name
	def __init__(self, name):
		global currentInputCollector
		currentInputCollector = self
		self.name = name
	def eventIsNumber(self, event):
		global inputNumbers
		maxLength = 3
		if int(event.unicode) in range(10):
			if len(inputNumbers) < maxLength:
				inputNumbers.append(event.unicode)
			elif len(inputNumbers) == maxLength:
				print("Hit submit or edit your entry.")
			return True
		else:
			return False
	def getInputData(self):
		##First, collector grabs current time
		currentTime = ""
		now = datetime.now()
		dateUnits = [now.year, now.month, now.day, now.hour, now.minute]
		for unit in dateUnits:
			unit = str(unit)
			if len(unit) < 2:
				unit = "0%s" % unit
			currentTime = currentTime + unit
		##Then, it grabs the datum type
		datumType = self.name
		##Finally, it compiles the input into a final value
		currentNumber = ""
		while len(currentNumber) < len(inputNumbers):
			for number in inputNumbers:
				currentNumber = currentNumber + number[0]
		##It returns a dictionary with every value
		inputData = {"Time": currentTime, "Type": datumType, "Value": currentNumber}
		return inputData
	def displayInput(self):
		offset = 0
		for number in inputNumbers:
			numberImage = pygame.image.load("%s.png" % number)
			screen.blit(numberImage, (offset, 0))
			offset += pygame.Surface.get_size(numberImage)[0]
	def submit(self):
		global inputNumbers
		if inputNumbers:
			newInput = Data.Datum(self.getInputData())
			storedValues.append(newInput)
		inputNumbers = []
	def collectInput(self, event):
		global inputNumbers
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				if len(inputNumbers) > 0:
					inputNumbers.pop()
			elif event.key == pygame.K_RETURN:
				self.submit()
			else:
				try:
					self.eventIsNumber(event)
				except ValueError:
					print("Unacceptable input.")

class Menu(): ##Takes optional buttons and optional position
	def __init__(self, buttons=None, position=None):
		self.buttons = buttons
		self.pos = position
	def displayMenu(self):
		for button in self.buttons:
			screen.blit(button.image, button.pos)
margin = 100
graph = Graph(SCREENWIDTH - margin, SCREENHEIGHT - margin, (50, 50), None)

class InputWindow(): ##Takes self, image, name, and optional position
	def cancelInput(self):
		global currentWindow, currentInputCollector, inputNumbers
		del(currentWindow)
		currentWindow = None
		del(currentInputCollector)
		currentInputCollector = None
		inputNumbers = []
		self.selected = False
	def submit(self):
		currentInputCollector.submit()
		self.selected = False
	def __init__(self, image, name, position=None):
		global currentWindow
		currentWindow = self
		self.image = pygame.image.load(image)
		self.size = pygame.Surface.get_size(self.image)
		self.name = name
		self.pos = position

		add = Button("add.png", name="add")
		add.pos = (SCREENWIDTH - add.size[0], 85)
		add.updateBounds()
		add.action = InputWindow.submit

		cancel = Button("cancel.png", name="cancel")
		cancel.pos = (SCREENWIDTH - cancel.size[0], 100)
		cancel.updateBounds()
		cancel.action = InputWindow.cancelInput

		self.buttons = [add, cancel]
		InputCollector(name)

	def displayInputWindow(self):
		screen.blit(self.image, self.pos)
		for button in self.buttons:
			screen.blit(button.image, button.pos)


def setupAddMenu():
	addMenu = Menu()

	def inputSelectionAction(button):
		inputWindowPos = (SCREENWIDTH - 150, 0)
		newField = InputWindow("%s Input Field.png" % button.name, button.name, position=inputWindowPos)
		button.selected = False

	bloodSugarButton = Button("Blood Sugar Button.png", name = "Blood Sugar", action = inputSelectionAction)
	insulinDoseButton = Button("Insulin Dose Button.png", name = "Insulin Dose", action = inputSelectionAction)
	foodConsumptionButton = Button("Food Consumption Button.png", name = "Food Consumption", action = inputSelectionAction)
	addMenu.buttons = [bloodSugarButton, insulinDoseButton, foodConsumptionButton]

	addMenu.pos = (SCREENWIDTH - bloodSugarButton.size[0], 0)

	i = 0
	for button in addMenu.buttons:
		buttonX = 0 + addMenu.pos[0]
		buttonY = button.size[1] * i + addMenu.pos[1]
		i += 1
		button.pos = (buttonX, buttonY)
		button.updateBounds()
	return addMenu
addMenu = setupAddMenu()

def isButtonPressed(event):
	if event.type == pygame.MOUSEBUTTONUP:
		for button in buttons:
			inX = False
			inY = False
			if button.xbounds[0] < event.pos[0] < button.xbounds[1]:
				inX = True
			if button.ybounds[0] < event.pos[1] < button.ybounds[1]:
				inY = True
			if inX and inY:
				button.selected = True

def setupGraphControl():
	graphControl = Menu()
	buttonX = (SCREENWIDTH/2) - (100 / 2)
	buttonY = 25
	month = Button("Month.png", name = 'month', position = (buttonX, buttonY), action = Graph.Range.changeUnit)
	day = Button("Day.png", name = 'day', position = (buttonX, buttonY), action = Graph.Range.changeUnit)
	hour = Button("Hour.png", name = 'hour', position = (buttonX, buttonY), action = Graph.Range.changeUnit)
	leftArrow = Button("LeftArrow.png", position = (month.pos[0] - 50, buttonY), action = Graph.Range.changeStart)
	rightArrow = Button("RightArrow.png", position = (month.xbounds[1], buttonY), action = Graph.Range.changeStart)
	graphControl.buttons = [hour, day, month, leftArrow, rightArrow]
	return graphControl
graph.menu = setupGraphControl()

while running:
	pygame.Surface.fill(screen, (0x445566))
	graph.displayGraph()
	addMenu.displayMenu()

	if currentInputCollector:
		currentInputCollector.displayInput()
	if currentWindow:
		currentWindow.displayInputWindow()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Data.add()
			running = False
		isButtonPressed(event)
		if currentInputCollector:
			currentInputCollector.collectInput(event)

	for button in buttons:
		if button.selected:
			try:
				button.action()
			except TypeError:
				button.action(button)

	pygame.display.flip()
	clock.tick(20)
sys.exit()()