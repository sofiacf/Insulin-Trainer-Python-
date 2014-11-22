import pygame
import sys
import pickle
import datetime
pygame.init()


def Setup():
	global width, height, screen, key, graph
	global zero, one, two, three, four, five, six, seven, eight, nine, numbers
	global inputNumbers, firstNumber, secondNumber, thirdNumber, storedNumbers
	(width, height) = (500, 500)
	screen = pygame.display.set_mode((width, height))
	key = pygame.key.get_pressed()
	pygame.display.set_caption("This is the python version of Insulin Trainer")
	graph = pygame.Surface((width-100, height-100))

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

	def loadData():
		inputDataObject = open("Blood Sugar Data.txt", 'rb')
		return pickle.load(inputDataObject)
		inputDataObject.close()

	storedNumbers = loadData()
	currentNumber = ""
	inputNumbers = []
	firstNumber = [None, (0, 0)]
	secondNumber = [None, (10, 0)]
	thirdNumber = [None, (20, 0)]
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

class AddMenu(Button):
	def __init__(self, image, inputID, isSelected, commonName, field):
		self.image = image
		self.id = inputID
		self.selected = isSelected
		self.name = commonName
		self.pos = (width - pygame.Surface.get_size(self.image)[0], pygame.Surface.get_size(self.image)[1] * self.id)
		self.size = pygame.Surface.get_size(self.image)
		self.field = field
		self.fieldpos = (width - pygame.Surface.get_size(self.field)[0], 0)
		self.type = "AddMenuButton"
def AddMenuSetup():
	global bloodSugarButton, insulinDoseButton, foodConsumptionButton, MenuButtons, allTheButtons
	bloodSugarButton = AddMenu((pygame.image.load("Blood Sugar Button.png")), 0, False, "Blood Sugar", pygame.image.load("Blood Sugar Input Field.png"))
	insulinDoseButton = AddMenu((pygame.image.load("Insulin Dose Button.png")), 1, False, "Insulin Dose", pygame.image.load("Insulin Dose Input Field.png"))
	foodConsumptionButton = AddMenu((pygame.image.load("Food Consumption Button.png")), 2, False, "Food Consumption", pygame.image.load("Food Consumption Input Field.png"))
	MenuButtons = [bloodSugarButton, foodConsumptionButton, insulinDoseButton]
AddMenuSetup()

class Data():
	def __init__(self, arg):
		self.arg = arg
		

allTheButtons = [bloodSugarButton, foodConsumptionButton, insulinDoseButton, add, cancel]

def displayMenuButtons():
	for button in MenuButtons:
		screen.blit(button.image, button.pos)
def isButtonPressed():
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
def displayInputWindow():
	for button in MenuButtons:
		if button.selected == True and cancel.selected == False:
			screen.blit(button.field, button.fieldpos)
			screen.blit(cancel.image, cancel.pos)
			screen.blit(add.image, add.pos)
			return True
		elif cancel.selected == True:
			return False
def collectInput(event):
	global firstNumber, secondNumber, thirdNumber, inputNumbers
	numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	if displayInputWindow():
		if event.type == pygame.KEYDOWN:
			if event.unicode in numbers:
				if firstNumber[0] == None:
					firstNumber[0] = event.unicode
					inputNumbers.append(firstNumber)
				elif secondNumber[0] == None:
					secondNumber[0] = event.unicode
					inputNumbers.append(secondNumber)
				elif thirdNumber[0] == None:
					thirdNumber[0] = event.unicode
					inputNumbers.append(thirdNumber)
			elif event.key == pygame.K_BACKSPACE:
				if thirdNumber[0]:
					thirdNumber[0] = None
				elif secondNumber[0]:
					secondNumber[0] = None
				elif firstNumber[0]:
					firstNumber[0] = None
				if len(inputNumbers) != 0: 
					inputNumbers.pop()
			elif event.key == pygame.K_RETURN:
				submit()
			else:
				print("That is not acceptable input. Please try again with a /NUMBER/.")
def displayInput(): 
	if displayInputWindow():  
		for number in numbers:
			if str(number.value) == firstNumber[0]:
				screen.blit(number.image, firstNumber[1])
			if str(number.value) == secondNumber[0]:
				screen.blit(number.image, secondNumber[1])
			if str(number.value) == thirdNumber[0]:
				screen.blit(number.image, thirdNumber[1])
def getCurrentNumber():
	currentNumber = ""
	if len(currentNumber) < len(inputNumbers):
		for inputnumber in inputNumbers:
				currentNumber = currentNumber + inputnumber[0]
	if len(currentNumber) >= 1:
		currentNumber = str(currentNumber)
	return currentNumber
def submit():
	global storedNumbers
	currentNumber = getCurrentNumber()
	if len(currentNumber) >= 1:
		storedNumbers.append([currentNumber, datetime.datetime.now()])
	inputData = "Blood Sugar Data.txt"
	inputDataObject = open(inputData, 'wb')
	pickle.dump(storedNumbers, inputDataObject)
	inputDataObject.close()

	inputDataObject = open("Blood Sugar Data.txt", 'rb')
	print(pickle.load(inputDataObject))
	inputDataObject.close()
	return storedNumbers
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