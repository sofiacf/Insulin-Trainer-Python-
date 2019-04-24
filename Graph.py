import pygame
pygame.init()

def Setup():
	global width, height, screen, graph
	(width, height) = (500, 500)
	screen = pygame.display.set_mode((width, height))
	graph = pygame.draw.rect(screen, (0,0,0), (50, 50, 50, 50))
	pygame.display.set_caption("This is the map. I'm writing it here because stuff.")
Setup()



graph = pygame.Surface((width-100, height-100))
screen.blit(graph, (50, 50))

running = True
while running:
	pygame.Surface.fill(screen, (0x445566))
	pygame.event.get()
	pygame.event.pump
	screen.blit(graph, (50, 50))
	graph.fill((0,0,0))
	graph.blit(pygame.image.load("img/Sample Image.jpg"), (0,0))
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
