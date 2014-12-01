import pygame
import sys
import json
from datetime import datetime
pygame.init()
def Setup():
	global width, height, screen, key, numbers
	global currentNumber, inputNumbers, storedValues, aValueHasBeenSubmittedRecently
	(width, height) = (500, 500)
	screen = pygame.display.set_mode((width, height))
	key = pygame.key.get_pressed()
	pygame.display.set_caption("Insulin Trainer")
	class Number():
		def __init__(self, value):
			self.image = pygame.image.load("%s.png" %value)
			self.value = value
		def setupNumbers():
			numbers = []
			for number in range(10):
				number = Number(number)
				numbers.append(number)
			return numbers
	numbers = Number.setupNumbers()

	try:
		storedValues = Data.update()
	except ValueError:
		storedValues = []

	aValueHasBeenSubmittedRecently = False

	currentNumber = ""
	inputNumbers = []
class Data():
	def __init__(self, date, inputType, value):
		self.date = date
		self.type = inputType
		self.value = value
	def add(value):
		inputFile = "Blood Sugar Data.txt"
		inputFileObject = open(inputFile, 'w')
		json.dump(value, inputFileObject)
		inputFileObject.close()
	def update():
		inputFile = "Blood Sugar Data.txt"
		inputFileObject = open(inputFile, 'r')
		return json.load(inputFileObject)
		inputFileObject.close()
Setup()
class Button(): ##Other control buttons
	def __init__(self, image, isSelected, commonName, position):
		self.image = pygame.image.load(image)
		self.selected = isSelected
		self.name = commonName
		self.pos = position
		self.size = pygame.Surface.get_size(self.image)

class AddMenu():
	def __init__(self):
		bloodSugarButton = Button("Blood Sugar Button.png", False, "Blood Sugar", None)
		insulinDoseButton = Button("Insulin Dose Button.png", False, "Insulin Dose", None)
		foodConsumptionButton = Button("Food Consumption Button.png", False, "Food Consumption", None)
		self.menuButtons = [bloodSugarButton, insulinDoseButton, foodConsumptionButton]
		getButtonPosition(self.menuButtons)
	def getButtonPosition(buttonSet):
		i = 0
		for button in buttonSet:
			button.position = (width - button.size[0], button.size[1] * i)
			i += 1
	def displayMenuButtons(self): ##Blits the usual menu buttons.
		for button in self.menuButtons:
			screen.blit(button.image, button.pos)

menuButtons = [bloodSugarButton, insulinDoseButton, foodConsumptionButton]
otherButtons = [cancel, add]
class InputField():
	def __init__(self, image, pairedButton):
		self.image = pygame.image.load(image)
		self.size = pygame.Surface.get_size(self.image)
		self.pos = (width - self.size[0], 0)
		self.button = pairedButton
def inputFieldSetup():
	global bloodSugarField, insulinDoseField, foodConsumptionField
	bloodSugarField = InputField("Blood Sugar Input Field.png", bloodSugarButton)
	insulinDoseField = InputField("Insulin Dose Input Field.png", insulinDoseButton)
	foodConsumptionField = InputField("Food Consumption Input Field.png", foodConsumptionButton)
inputFieldSetup()
inputFields = [bloodSugarField, insulinDoseField, foodConsumptionField]
class Graph():
	def __init__(self, width, height, position, color, content):
		self.width = width
		self.height = height
		self.size = (self.width, self.height)
		self.position = position
		self.color = color
		self.content = content
		self.Surface = pygame.Surface(self.size)
		self.myrange = Graph.Range('hour', 201411232000)
		print("constructing a graph")
	class Range():
		def __init__(self, unit, start, points=[]):
			unitConversion = {'year': 100000000, 'month': 1000000, 'day': 10000, 'hour': 60}
			self.unit = unit
			self.convertedunit = unitConversion[unit]
			self.start = start
			self.points = points
	def graphControl(self):
		# def __init__(self):
		# 	self.placeHolderRangeButton = RangeButton(pygame.image.load("Hour.png"), 'hour')
		global placeHolderRangeButton, rangeHasRecentlyBeenChanged
		class RangeButton():
			def __init__(self, image, rangeattributematcher, isSelected = False):
				self.image = image
				self.size = pygame.Surface.get_size(image)
				self.width = self.size[0]
				self.height = self.size[1]
				self.rangeattributematcher = rangeattributematcher
				self.xpos = (width / 2) - (self.width / 2)
				self.ypos = 50 - self.height
				self.pos = (self.xpos, self.ypos)
				self.selected = isSelected
		hour = RangeButton(pygame.image.load("Hour.png"), 'hour')
		day = RangeButton(pygame.image.load("Day.png"), 'day')
		month = RangeButton(pygame.image.load("Month.png"), 'month')
		rangeButtons = [hour, day, month]
		try:
			placeHolderRangeButton
		except NameError:
			placeHolderRangeButton = RangeButton(pygame.image.load("Hour.png"), 'hour') ##For isSelected
		def displayRangeControl(self):
			for button in rangeButtons:
				if self.myrange.unit == button.rangeattributematcher:
					screen.blit(button.image, (button.xpos, button.ypos))
		def setRange():
			possibleUnits = ['hour', 'day', 'month']
			i = 0
			for possibleunit in possibleUnits:
				if self.myrange.unit == possibleunit:
					if i < len(possibleUnits) - 1:
						self.myrange.unit = possibleUnits[i + 1]
					else: self.myrange.unit = possibleUnits[0]
				else: i += 1
		displayRangeControl()
		if placeHolderRangeButton.selected == True and rangeHasRecentlyBeenChanged == False:
			rangeHasRecentlyBeenChanged = True
			setRange()
			placeHolderRangeButton.selected = False
	def displayGraph(self): ##Blits a graph, and does a shit ton of stuff with ranges and points lulz
		screen.blit(self.Surface, self.position)
		self.Surface.fill(self.color)
		def getPointsInRange(): ##Sets points attribute for a range object
			self.myrange.points = []
			for datapoint in storedValues:
				if self.myrange.start < int(datapoint['InputTime']) < self.myrange.start + self.myrange.convertedunit:
					self.myrange.points.append(datapoint)
		def convertValueToPosition(): ##Returns list of dicts points as w/ type and pos
			heightConverter = 1.6
			pointsToGraph = []
			posPointDivisor = self.myrange.convertedunit / self.width
			xmax = self.myrange.start + self.myrange.convertedunit
			for datapoint in self.myrange.points:
				xpos = int((((xmax - int(datapoint['InputTime'])) / self.myrange.convertedunit) * self.width))
				if datapoint['InputType'] == "Blood Sugar":
					ypos = int((int(datapoint['InputValue']) * heightConverter))
				else:
					ypos = (50)
				pointsToGraph.append({'point type': datapoint['InputType'], 'position': (xpos, ypos)})
			return pointsToGraph

		inputSymbols = {"Blood Sugar": pygame.image.load("Blood Sugar Point.png"), "Insulin Dose" : pygame.image.load("Insulin Dose Point.png"), "Food Consumption": pygame.image.load("Food Consumption Point.png")}
		pointCenterCorrector = (pygame.Surface.get_size(pygame.image.load("Blood Sugar Point.png"))[0]/2)

		def convertComplexPointDictToList(pointDict): ##Converts point dict to list of draw.aalines-compatible tuples
			drawablePointList = []
			for pointListing in pointDict:
				newtuple = (pointListing['position'])
				drawablePointList.append(newtuple)
			return drawablePointList
		def plotPoints(points): ##Blits points from pointsToGraph, pos corrected to center; draws connecting lines
			pygame.draw.aalines(self.Surface, (250, 0, 0), False, convertComplexPointDictToList(points))
			for point in points:
				if point['point type'] == "Blood Sugar":
					self.Surface.blit(inputSymbols["Blood Sugar"], ((point['position'][0] - pointCenterCorrector), point['position'][1] - pointCenterCorrector))
		getPointsInRange()
		convertValueToPosition()
		pointsToGraph = convertValueToPosition()
		plotPoints(pointsToGraph)
		drawablePointList = convertComplexPointDictToList(pointsToGraph)
myGraph = Graph(width - 100, height - 100, (50, 50), (0, 0, 0), None)
# allTheButtons = [bloodSugarButton, foodConsumptionButton, insulinDoseButton, add, cancel] ##, placeHolderRangeButton]
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
			else: button.selected = False
			if add.selected == True and aValueHasBeenSubmittedRecently == False:
				submit()
				aValueHasBeenSubmittedRecently = True
				add.selected = False
	else: aValueHasBeenSubmittedRecently = False; rangeHasRecentlyBeenChanged = False
def displayInputWindow(): ##Shows the input screen until cancel.
	global currentNumber
	for button in menuButtons:
		if button.selected == True and cancel.selected == False:
			screen.blit(button.field, button.fieldpos)
			screen.blit(cancel.image, cancel.pos)
			screen.blit(add.image, add.pos)
			button.displayed = True
			return True
		elif cancel.selected == True:
			button.selected = False
			currentNumber = []
			return False
def collectInput(event): ##Adds numbers to inputNumbers; calls submit
	global inputNumbers
	numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	if displayInputWindow():
		if event.type == pygame.KEYDOWN:
			if event.unicode in numbers and len(inputNumbers) < 3:
				targetIndex = len(inputNumbers)
				inputNumbers.append([event.unicode, (targetIndex * 10, 0)])
			elif event.key == pygame.K_BACKSPACE and len(inputNumbers) != 0:
				inputNumbers.pop()
			elif event.key == pygame.K_RETURN:
				submit()
			else:
				print("That is not acceptable input. Please try again with a /NUMBER/.")
def displayInput(): ##Blits numbers as user types, COULD MAYBE BE BETTER. NEXT THING TO LOOK AT
	if displayInputWindow() and len(inputNumbers) > 0:  
		for number in numbers:
			for inputNumber in inputNumbers:
				if str(number.value) == inputNumber[0]:
					screen.blit(number.image, inputNumber[1])
def submit(): ##Creates storedValues dict and calls Data.add() on it
	global storedValues, currentNumber
	def getCurrentNumber():
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
					inputType = button.name
			return inputType
	inputType = getInputType()
	if len(currentNumber) >= 1:	
		storedValues.append({'InputValue': currentNumber, 'InputTime': currentTime, 'InputType': inputType})
	Data.add(storedValues)
clock = pygame.time.Clock()
running = True
while running:
	key = pygame.key.get_pressed()
	pygame.Surface.fill(screen, (0x445566))
	myGraph.displayGraph()
	# myGraph.graphControl()
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