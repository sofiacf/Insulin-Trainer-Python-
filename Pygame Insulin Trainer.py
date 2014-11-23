import pygame
import sys
import json
import datetime
pygame.init()

def Setup():
	global width, height, screen, key, graph
	global zero, one, two, three, four, five, six, seven, eight, nine, numbers
	global inputNumbers, storedNumbers
	global now
	(width, height) = (500, 500)
	screen = pygame.display.set_mode((width, height))
	key = pygame.key.get_pressed()
	pygame.display.set_caption("This is the python version of Insulin Trainer")
	graph = pygame.Surface((width-100, height-100))
	now = datetime.datetime.now()
	print()
	class Number():
		def __init__(self, name, image, value):
			self.name = name
			self.image = image
			self.value = value
	zero = Number(pygame.K_0, pygame.image.load("0.png"), 0)
	one = Number(pygame.K_1, pygame.image.load("1.png"), 1)
	two = Number(pygame.K_2, pygame.image.load("2.png"), 2)
	three = Number(pygame.K_3, pygame.image.load("3.png"), 3)
	four = Number(pygame.K_4, pygame.image.load("4.png"), 4)
	five = Number(pygame.K_5, pygame.image.load("5.png"), 5)
	six = Number(pygame.K_6, pygame.image.load("6.png"), 6)
	seven = Number(pygame.K_7, pygame.image.load("7.png"), 7)
	eight = Number(pygame.K_8, pygame.image.load("8.png"), 8)
	nine = Number(pygame.K_9, pygame.image.load("9.png"), 9)
	numbers = [zero, one, two, three, four, five, six, seven, eight, nine]
	if Data.update():
		storedNumbers = [Data.update()]
	else: storedNumbers = []
	currentNumber = ""
	inputNumbers = []
class Data():
	def __init__(self, date, inputtype, value):
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
class Button():
	def __init__(self, image, isSelected, commonName, yOffset):
		self.image = image
		self.selected = isSelected
		self.name = commonName
		self.yOffset = yOffset
		self.pos = (width - pygame.Surface.get_size(self.image)[0], yOffset)
		self.size = pygame.Surface.get_size(self.image)
		self.type = Button
def ButtonSetup():
	global cancel, add
	cancel = Button(pygame.image.load("cancel.png"), False, "cancel", 100)
	add = Button(pygame.image.load("add.png"), False, "add", 85)
ButtonSetup()

class AddMenu(Button): ##This class sets up the buttons that open up the input fields
	def __init__(self, image, inputID, isSelected, commonName, field, displayed):
		self.image = image
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
	bloodSugarButton = AddMenu((pygame.image.load("Blood Sugar Button.png")), 0, False, "Blood Sugar", pygame.image.load("Blood Sugar Input Field.png"), False)
	insulinDoseButton = AddMenu((pygame.image.load("Insulin Dose Button.png")), 1, False, "Insulin Dose", pygame.image.load("Insulin Dose Input Field.png"), False)
	foodConsumptionButton = AddMenu((pygame.image.load("Food Consumption Button.png")), 2, False, "Food Consumption", pygame.image.load("Food Consumption Input Field.png"), False)
	MenuButtons = [bloodSugarButton, foodConsumptionButton, insulinDoseButton]
AddMenuSetup()

allTheButtons = [bloodSugarButton, foodConsumptionButton, insulinDoseButton, add, cancel]

def displayMenuButtons(): ##This is always blitting the usual menu buttons.
	for button in MenuButtons:
		screen.blit(button.image, button.pos)
def isButtonPressed(): ##This needs fixing.
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
def displayInputWindow(): ##If you clicked on a button, it'll show the input screen :D Unless the button was cancel.
	global currentNumber
	for button in MenuButtons:
		if button.selected == True and cancel.selected == False:
			screen.blit(button.field, button.fieldpos)
			screen.blit(cancel.image, cancel.pos)
			screen.blit(add.image, add.pos)
			button.displayed = True
			return True
		elif cancel.selected == True:
			currentNumber = []
			return False
def collectInput(event): ##Gets keydown events and adds numbers to inputNumbers array; calls submit on enter
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
def displayInput(): ##Blits numbers as user types them -- as long as there's at least one...
	if displayInputWindow() and len(inputNumbers) > 0:  
		for number in numbers:
			for inputNumber in inputNumbers:
				if str(number.value) == inputNumber[0]:
					screen.blit(number.image, inputNumber[1])
def getCurrentNumber(): ##Gets inputNumbers array from submit and returns it as string 'currentNumber"
	currentNumber = ""
	if len(currentNumber) < len(inputNumbers):
		for inputnumber in inputNumbers:
				currentNumber = currentNumber + inputnumber[0]
	if len(currentNumber) >= 1:
		currentNumber = str(currentNumber)
	return currentNumber
def submit(): ##On enter, appends currentNumber to storedNumbers and dumps it to the .. file.. 
	global storedNumbers
	currentNumber = getCurrentNumber()
	currentDate = str(datetime.datetime.now())
	if len(currentNumber) >= 1:
		storedNumbers.append([currentNumber, currentDate])
	Data.add(storedNumbers)
	# inputDataObject = open("Blood Sugar Data.txt", 'r')
	# print(json.load(inputDataObject))
	# inputDataObject.close()
	# return storedNumbers
	def getInputType():
		for button in MenuButtons:
			if button.displayed == True:
				inputType = button.name
				return inputType

sampleImage = pygame.image.load("Sample Image.jpg")
clock = pygame.time.Clock()
running = True
while running:
	key = pygame.key.get_pressed()
	pygame.Surface.fill(screen, (0x445566))
	screen.blit(graph, (50, 50))
	graph.fill((0,0,0))
	graph.blit(sampleImage, (0,0))
	displayMenuButtons()
	isButtonPressed()
	displayInputWindow()
	displayInput()
	getCurrentNumber()
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		else:
			collectInput(event)
	clock.tick(20)
sys.exit()