import random, pygame, pygame.gfxdraw

# simulation variables
dt = 0.05
damping = 1
width, height = (1500, 700)
ballmax = 4

class Object():
    
    def __init__(self, number, colour, x, y, velocityx, velocityy, acceleration, radius):
        self.x = x
        self.y = y
        self.velx = velocityx
        self.vely = velocityy
        self.acc = acceleration
        self.colour = colour 
        self.radius = radius
        self.num = number
        self.KE = 0
    
    def posupdate(self):
        self.x += self.velx * dt
        self.y += self.vely * dt
        self.PE = 1/2 * (-1 * self.y + height - self.radius) ** 2
    
    def velupdate(self):

        # kinetic and potential energy
        self.vely += self.acc * dt
        self.KE = 1/2 * (self.velx**2 + self.vely**2)

        # checking for floor and bounce
        if self.y > height - self.radius:

            self.vely = self.vely * -1 * damping
            self.y = height - self.radius

        elif self.x < self.radius:
            self.velx = self.velx * -1 * damping
            self.x = self.radius

        elif self.x > width - self.radius:
            self.velx = self.velx * -1 * damping
            self.x = width - self.radius
        
        elif self.y < self.radius:
            self.vely = self.vely * -1 * damping
            self.y = self.radius

            #self.display()
        else:
            pass

    def display(self):
        print(f"""
            x: {self.x}
            y: {self.y}
            x velocity: {round(self.velx, 2)}
            y velocity: {round(self.vely, 2)}
            acceleration: {self.acc}
            Kinetic Energy: {round(self.KE, 3)}
            Potential Energy: {round(self.PE, 2)}
                """)
    def drawEnergy(self, screen):
        pygame.draw.line(screen, (255,0,0), (5,height), (5, (height - round(100*self.KE/13000))), 10)
        pygame.draw.line(screen, (0,255,0), (16,height), (16, (height - round((800/685)*self.PE))), 10)

    def connect(self, screen, balllist, number):
        
        for l in range(1, ballmax-1):
            if number == l:
                pass

            else:
                pygame.draw.line(screen, (0,0,0), (round(self.x), round(self.y)), (round(balllist[l].x), round(balllist[l].y)), round((((self.x - self.y)**2 + (balllist[l].x - balllist[l].y)**2)**0.5)/800)*10+1)
                print(round((((self.x - self.y)**2 + (balllist[l].x - balllist[l].y)**2)**0.5)))
                
        

def main():

    #pygame initialization
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('kinematic simulation')
    alpha = [0]
    for i in range(0,ballmax):
        alpha.append(random.randint(0,255))

    balllist = []
    for i in range(1,ballmax):
        balllist.append(Object(i, (random.randint(0,254),0,0), random.randint(5, 1485), random.randint(115,685), random.randint(-100,100), 0, 10, 3))
        

    # main loop
    running = True
    while running:

        # quit on escape
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # main clock for the simulation
        clock.tick(144)

        screen.fill((255,255,255))

        # update loop
        for i in range(1,ballmax - 1):
            pygame.gfxdraw.filled_circle(screen, round(balllist[i].x), round(balllist[i].y), balllist[i].radius, (round(255*balllist[i].KE/13000),0,0))
            pygame.gfxdraw.filled_circle(screen, round(balllist[i].x), round(balllist[i].y), balllist[i].radius, (0,0,round(255*balllist[i].KE/15000)))
            balllist[i].posupdate()
            balllist[i].velupdate()
            balllist[i].connect(screen, balllist, i)
        
        pygame.display.update()

main()