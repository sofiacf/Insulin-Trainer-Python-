import pygame
import sys
import json
from datetime import datetime
pygame.init()
def Setup():
	global SCREENWIDTH, SCREENHEIGHT, screen, storedValues, numbers, today, clock, inputNumbers, buttons
	(SCREENWIDTH, SCREENHEIGHT) = (500, 500)
	screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
	pygame.display.set_caption("Insulin Trainer 2")
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

	try:
		storedValues = Data.update()
	except ValueError:
		storedValues = []
	inputNumbers = []
	buttons = []
	def getTodaysDate():
		today = ""
		now = datetime.now()
		dateAttributes = [now.year, now.month, now.day]
		for attribute in dateAttributes:
			attribute = str(attribute)
			if len(attribute) < 2:
				attribute = "0%s" % attribute
			today = today + attribute
		return int(today + "0000")
	today = getTodaysDate()
	clock = pygame.time.Clock()
class Data():
	class Datum():
		def __init__(self, dictionary):
			self.time = int(dictionary['Time'])
			self.value = int(dictionary['Value'])
			self.type = dictionary['Type']	
	def add():
		dataToAdd = []
		for datum in storedValues:
			datumDict = {"Time": datum.time, "Value": datum.value, "Type": datum.type}
			dataToAdd.append(datumDict)
		database = "Blood Sugar Data.txt"
		databaseObject = open(database, 'w')
		json.dump(dataToAdd, databaseObject)
		databaseObject.close()
	def update():
		database = "Blood Sugar Data.txt"
		databaseObject = open(database, 'r')
		dataDictionary = json.load(databaseObject)
		storedValues = []
		for datum in dataDictionary:
			datum = Data.Datum(datum)
			storedValues.append(datum)
		databaseObject.close()
		return storedValues
Setup()
class Button():
	def __init__(self, image, isSelected = False, position = (0,0), action = print("No action set."), name = None):
		self.image = pygame.image.load(image)
		self.selected = isSelected
		self.size = pygame.Surface.get_size(self.image)
		self.pos = position
		self.xbounds = (position[0], position[0] + self.size[0])
		self.ybounds = (position[1], position[1] + self.size[1])
		self.action = action
		self.name = name
	def performAction(self):
		try:
			self.action(self)
		except TypeError:
			self.action()
	def updateBounds(self):
		self.xbounds = (self.pos[0], self.pos[0] + self.size[0])
		self.ybounds = (self.pos[1], self.pos[1] + self.size[1])
class InputCollector:
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
	def collectInputNumbers(event):
		def isEventANumber(event):
			if int(event.unicode) in range(10):
				if len(inputNumbers) < 3:
					inputNumbers.append(event.unicode)
				elif len(inputNumbers) == 3:
					print("Please submit input or delete a number.")
				return True
			else:
				return False
		global inputNumbers
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				if len(inputNumbers) > 0:
					inputNumbers.pop()
			elif event.key == pygame.K_RETURN:
				newInput = Input()
				add.selected = True
				inputNumbers = []
			else:
				try:
					isEventANumber(event)
				except ValueError:
					print("That is not acceptable input. Please enter a number, submit, or delete.")
class Input():
	def __init__(self):
		def getCurrentNumber():
			currentNumber = ""
			while len(currentNumber) < len(inputNumbers):
				for number in inputNumbers:
					currentNumber = currentNumber + number[0]
			return str(currentNumber)
		def getCurrentTime():
			currentTime = ""
			now = datetime.now()
			dateAttributes = [now.year, now.month, now.day, now.hour, now.minute]
			for attribute in dateAttributes:
				attribute = str(attribute)
				if len(attribute) < 2:
					attribute = "0%s" % attribute
				currentTime = currentTime + attribute
			return currentTime
		def getInputType():
			for button in addMenu.buttons:
				if button.selected == True:
					inputType = button.name
				return inputType
		self.currentNumber = getCurrentNumber()
		self.time = getCurrentTime()
		self.type = getInputType()
	def createAndAddNewDatum(self):
		if len(self.currentNumber) > 0:
			newDatum = {"Value": self.currentNumber, "Time": self.currentTime, "Type": self.inputType}
			storedValues.append(Data.Datum(newDatum))
class Menu():
	def __init__(self, buttons=None, position=None, action = None):
		self.buttons = buttons
		self.pos = position
		self.action = action
	def displayMenu(self):
		for button in self.buttons:
			screen.blit(button.image, button.pos)
class Graph():
	class Point(Data.Datum):
		def __init__(self, time, value, datumType):
			pointImages = {"Blood Sugar": pygame.image.load("Blood Sugar Point.png"), "Insulin Dose" : pygame.image.load("Insulin Dose Point.png"), "Food Consumption": pygame.image.load("Food Consumption Point.png")}
			self.time = time
			self.value = value
			self.type = datumType
			self.image = pointImages[self.type]
			self.size = pygame.Surface.get_size(self.image)
			self.pos = (87)
	class Range():
		def __init__(self, unit, start, points = []):
			unitConversion = {'year': 12000000, 'month': 310000, 'day': 2400, 'hour': 60}
			self.unit = unit
			self.convertedunit = unitConversion[unit]
			self.start = start
			self.cutoff = start + self.convertedunit
			self.points = []
		def changeUnit(button):
			unitConversion = {'year': 12000000, 'month': 310000, 'day': 2400, 'hour': 60}
			graph.timeRange.unit = button.name
			graph.timeRange.convertedunit = unitConversion[button.name]
		def changeStart(button):
			if button.pos[0] == ((SCREENWIDTH/2) - (100 / 2) - 50, 25): ##leftArrow
				direction = -1
			else:
				direction = 1
			graph.timeRange.start = graph.timeRange.start + graph.timeRange.convertedunit*direction
	def __init__(self, width, height, position, menu, timeRange = Range('day', today)):
		self.width = width
		self.height = height
		self.size = (width, height)
		self.pos = position
		self.menu = menu
		self.color = (0, 0, 0)
		self.Surface = pygame.Surface(self.size)
		self.timeRange = timeRange
	def getPoints(self):
		for datum in storedValues:
			if self.timeRange.start < datum.time < self.timeRange.cutoff:
				newPoint = Graph.Point(datum.time, datum.value, datum.type)
				self.timeRange.points.append(newPoint)
	def setPointPositions(self):
		heightConverter = 1.6
		posPointDivisor = self.timeRange.convertedunit / self.width
		xmax = graph.timeRange.cutoff
		for point in self.timeRange.points:
			xpos = self.width - int(self.width * (xmax - point.time) / self.timeRange.convertedunit)
			if point.type == "Blood Sugar":
				ypos = graph.height - int(point.value * heightConverter)
			else:
				ypos = 50
			point.pos = (xpos, ypos)
	def plotPoints(self):
		for point in self.timeRange.points:
			correctedPosition = (point.pos[0] + (point.size[0]/2), point.pos[1])
			self.Surface.blit(point.image, point.pos)
		lineDrawingList = []
		for point in self.timeRange.points:
			if point.type == "Blood Sugar":
				lineDrawingList.append(point.pos)
		lineDrawingList = sorted(lineDrawingList)
		if len(lineDrawingList) > 1:
			pygame.draw.aalines(self.Surface, (250, 0, 0), False, lineDrawingList)
	def displayGraph(self):
		screen.blit(self.Surface, self.pos)
		self.getPoints()
		self.setPointPositions()
		self.plotPoints()
class InputWindow():
	global submit, cancelInput
	def submit():
		newInput = Input()
		createAndAddNewDatum(newInput)
	def cancelInput():
		global inputNumbers, currentNumber
		inputNumbers = []
		currentNumber = ""
		return True
	def __init__(self, image,  position = None, displayed = False):
		global add, cancel, displayedInputWindow
		add = Button("add.png")
		add.pos = (SCREENWIDTH - add.size[0], 85)
		add.updateBounds()
		add.action = submit
		cancel = Button("cancel.png")
		cancel.pos = (SCREENWIDTH - cancel.size[0], 100)
		cancel.updateBounds()
		cancel.action = cancelInput
		self.image = pygame.image.load(image)
		self.size = pygame.Surface.get_size(self.image)
		self.pos = position
		self.buttons = [add, cancel]
		displayedInputWindow = self
	def displayInput(self):
		if len(inputNumbers) > 0:
			for number in numbers:
				i = 0
			for inputNumber in inputNumbers:
				if str(number.value) == inputNumber:
					screen.blit(number.image, (10 * i, 0))
				i += 1
	def displayInputWindow(self):
		self.displayInput()
		screen.blit(self.image, self.pos)
		for button in self.buttons:
			screen.blit(button.image, button.pos)
		return True
def setupAddMenu():
	global inputFields
	addMenu = Menu()
	bloodSugarButton = Button("Blood Sugar Button.png", name = "Blood Sugar")
	insulinDoseButton = Button("Insulin Dose Button.png", name = "Insulin Dose")
	foodConsumptionButton = Button("Food Consumption Button.png", name = "Food Consumption")
	addMenu.buttons = [bloodSugarButton, insulinDoseButton, foodConsumptionButton]
	addMenu.pos = (SCREENWIDTH - bloodSugarButton.size[0], 0)
	i = 0
	for button in addMenu.buttons:
		buttonX = 0 + addMenu.pos[0]
		buttonY = button.size[1] * i + addMenu.pos[1]
		i += 1
		button.pos = (buttonX, buttonY)
		button.updateBounds()
	bloodSugarField = InputWindow("Blood Sugar Input Field.png")
	bloodSugarField.pos = (SCREENWIDTH - bloodSugarField.size[0], 0)
	insulinDoseField = InputWindow("Insulin Dose Input Field.png")
	insulinDoseField.pos = (SCREENWIDTH - insulinDoseField.size[0], 0)
	foodConsumptionField = InputWindow("Food Consumption Input Field.png")
	foodConsumptionField.pos = (SCREENWIDTH - foodConsumptionField.size[0], 0)
	bloodSugarButton.action = bloodSugarField.displayInputWindow
	insulinDoseButton.action = insulinDoseField.displayInputWindow
	foodConsumptionButton.action = foodConsumptionField.displayInputWindow
	inputFields = [bloodSugarField, insulinDoseField, foodConsumptionField]
	return addMenu
addMenu = setupAddMenu()
graph = Graph(SCREENWIDTH - 100, SCREENHEIGHT - 100, (50, 50), None)
def setupGraphControl():
	graphControl = Menu()
	buttonX = (SCREENWIDTH/2) - (100 / 2)
	buttonY = 50 - 25
	month = Button("Month.png", name = 'month', position = (buttonX, buttonY), action = Graph.Range.changeUnit)
	day = Button("Day.png", name = 'day', position = (buttonX, buttonY), action = Graph.Range.changeUnit)
	hour = Button("Hour.png", name = 'hour', position = (buttonX, buttonY), action = Graph.Range.changeUnit)
	leftArrow = Button("LeftArrow.png", position = (month.pos[0] - 50, buttonY), action = Graph.Range.changeStart)
	rightArrow = Button("RightArrow.png", position = (month.xbounds[1], buttonY), action = Graph.Range.changeStart)
	graphControl.buttons = [hour, day, month, leftArrow, rightArrow]
	return graphControl
graph.menu = setupGraphControl()
def setupButtonList():
	buttons = []
	for button in addMenu.buttons:
		buttons.append(button)
	for button in graph.menu.buttons:
		buttons.append(button)
	buttons.append(add)
	buttons.append(cancel)
	return buttons
buttons = setupButtonList()
def activateButtons():
	for button in buttons:
		if button.selected:
			button.performAction()
running = True
while running:
	pygame.Surface.fill(screen, (0x445566))
	graph.displayGraph()
	graph.menu.displayMenu()
	addMenu.displayMenu()
	activateButtons()
	pygame.display.flip()
	for event in pygame.event.get():
		InputCollector.isButtonPressed(event)
		InputCollector.collectInputNumbers(event)
		if event.type == pygame.QUIT:
			running = False
	clock.tick(20)
sys.exit()