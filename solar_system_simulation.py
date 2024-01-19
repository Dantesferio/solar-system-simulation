import math
import sys
import pygame


W, H = 1000,1000
FPS = 60
DELTA_T = 1/FPS
BLACK = (0,0,0)
WHITE = (255,255,255)
G = W/100
SCALE = (W/2) / 219
INITAL_VELOCITY = 500


pygame.init()
window = pygame.display.set_mode((W, H))
pygame.display.set_caption("planet orbeting simulation")
clock = pygame.time.Clock()


class Planet:
	def __init__(self, mass=1.0, size = 0.0, color = (255,255,255)) -> None:
		self.position = [0.0, 0.0]
		self.velocity = [0.0, 0.0]
		self.acceleration = 0
		self.mass = mass
		self.color = color
		self.size = size

	def move(self, delta_x, delta_y):
		self.position[0] += delta_x
		self.position[1] += delta_y

	def draw(self, win):
		pygame.draw.circle(win, self.color, self.position, self.size * 20)

	def calculate_gravity(self, sun):
		delta_x = 0
		delta_y = 0

		dx = self.position[0] - sun.position[0]
		dy = self.position[1] - sun.position[1]
		r = math.sqrt((dx*dx) + (dy*dy)) * (10**12)

		if r != 0:
			f = G * self.mass * sun.mass / (r*r)
		else: 
			f = G * self.mass * sun.mass / 0.001
		if f == 0:
			return (0, 0)

		alpha = math.atan2(dy, dx)

		acc = (f/self.mass) + self.acceleration
		#self.acceleration = acc
		ax = -acc * math.cos(alpha)
		ay = -acc * math.sin(alpha)

		vx2 = self.velocity[0] + (ax * DELTA_T)
		vy2 = self.velocity[1] + (ay * DELTA_T)
		self.velocity = [vx2, vy2]

		delta_x += vx2*DELTA_T
		delta_y += vy2*DELTA_T

		return (delta_x, delta_y)

class Sun(Planet):
	def __init__(self, mass, color) -> None:
		super().__init__(mass, color)
		self.position = [W/2, H/2]

	def draw(self, win):
		pygame.draw.circle(win,  (250, 172, 17), [W/2, H/2], 75)



sun = Sun(2 * (10**30), (250, 172, 17))

mercury = Planet(3.30 * (10**23), 0.383, (44,80,56))
venus = Planet(4.87 * (10**24), 0.949, (245, 203, 98))
earth = Planet(5.97 * (10**24), 1, (98, 179, 245))
mars = Planet(6.42 * (10**23), 0.532, (252, 104, 63))

mercury.position = [H/2 - 65*SCALE,H/2]
venus.position = [H/2 - 108*SCALE, H/2]
earth.position = [H/2 - 150*SCALE, H/2]
mars.position = [H/2 - 219*SCALE, H/2]

addition = 3
mercury.velocity = [0.0, 368]
venus.velocity = [0.0, 284]
earth.velocity = [0.0, 241]
mars.velocity = [0.0, 200]

planets = [sun, mercury, venus, earth, mars]


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)

	window.fill(BLACK)

	pygame.draw.circle(window, WHITE, [W/2, H/2], 65*SCALE, 1)
	pygame.draw.circle(window, WHITE, [W/2, H/2], 108*SCALE,1)
	pygame.draw.circle(window, WHITE, [W/2, H/2], 150*SCALE,1)
	pygame.draw.circle(window, WHITE, [W/2, H/2], 219*SCALE,1)

	for p in planets:
		p.draw(window)
		if not p == sun:
			delta_position = p.calculate_gravity(sun)
			p.move(delta_position[0], delta_position[1])

	pygame.display.update()
	clock.tick(FPS)