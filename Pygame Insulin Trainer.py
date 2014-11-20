import pygame
import sys
pygame.init()

def Setup():
	global width, height, screen, key, windowBlitted, graph
	global zero, one, two, three, four, five, six, seven, eight, nine, numbers, currentNumber, inputNumbers
	(width, height) = (500, 500)
	screen = pygame.display.set_mode((width, height))
	key = pygame.key.get_pressed()
	pygame.display.set_caption("This is the python version of Insulin Trainer")
	submit = False
	graph = pygame.Surface((width-100, height-100))
	inputNumbers = []
	currentNumber = ""
	font = pygame.font.Font(None, 14)
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
	global bloodSugarInputButton, insulinDoseButton, foodConsumptionButton, MenuButtons, allTheButtons
	bloodSugarInputButton = AddMenu((pygame.image.load("Blood Sugar Button.png")), 0, False, "Blood Sugar", pygame.image.load("Blood Sugar Input Field.png"))
	insulinDoseButton = AddMenu((pygame.image.load("Insulin Dose Button.png")), 1, False, "Insulin Dose", pygame.image.load("Insulin Dose Input Field.png"))
	foodConsumptionButton = AddMenu((pygame.image.load("Food Consumption Button.png")), 2, False, "Food Consumption", pygame.image.load("Food Consumption Input Field.png"))
	MenuButtons = [bloodSugarInputButton, foodConsumptionButton, insulinDoseButton]
AddMenuSetup()

allTheButtons = [bloodSugarInputButton, foodConsumptionButton, insulinDoseButton, add, cancel]

def displayMenuButtons():
	for button in MenuButtons:
		screen.blit(button.image, button.pos)

firstNumber = [None, (0, 0)]
secondNumber = [None, (10, 0)]
thirdNumber = [None, (20, 0)]
def displayInputWindow():
	for button in MenuButtons:
		if button.selected == True and cancel.selected == False:
			windowBlitted = True
			screen.blit(button.field, button.fieldpos)
			screen.blit(cancel.image, cancel.pos)
			screen.blit(add.image, add.pos)
			return True
		elif cancel.selected == True:
			return False
def collectInput(event):
	global firstNumber, secondNumber, thirdNumber, inputNumbers, currentNumber
	if displayInputWindow():
			if event.type == pygame.KEYDOWN:
				if firstNumber[0] == None:
					firstNumber[0] = event.unicode
					inputNumbers.append(firstNumber)
				elif secondNumber[0] == None:
					secondNumber[0] = event.unicode
					inputNumbers.append(secondNumber)
				elif thirdNumber[0] == None:
					thirdNumber[0] = event.unicode
					inputNumbers.append(thirdNumber)
def submit():
	global currentNumber
	for inputnumber in inputNumbers:
		if inputnumber[0] and len(currentNumber) <= 2:
			currentNumber = currentNumber + inputnumber[0]
	if len(currentNumber) >= 1:
		int(currentNumber)
def displayInput(): 
	if displayInputWindow():  
		for number in numbers:
			if str(number.value) == firstNumber[0]:
				screen.blit(number.image, firstNumber[1])
			if str(number.value) == secondNumber[0]:
				screen.blit(number.image, secondNumber[1])
			if str(number.value) == thirdNumber[0]:
				screen.blit(number.image, thirdNumber[1])
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

sampleImage = pygame.image.load("Sample Image.jpg")
clock = pygame.time.Clock()

running = True
while running:
	pygame.event.pump()
	key = pygame.key.get_pressed()
	pygame.Surface.fill(screen, (0x445566))
	screen.blit(graph, (50, 50))
	graph.fill((0,0,0))
	graph.blit(sampleImage, (0,0))
	displayMenuButtons()
	isButtonPressed()
	displayInputWindow()
	displayInput()
	submit()
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		else:
			collectInput(event)
	clock.tick(20)
sys.exit()