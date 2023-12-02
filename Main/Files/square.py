import random, pygame, pygame.gfxdraw, math

# simulation variables
dt = 0.025 # timestep
damping = 1 # damping due to loss of energy, not working
width, height = (1001, 701) # screen dimensions
ballmax = 2 # amount of balls
balllist = ballmax*[0] # empty list to contain ball objects

# class for balls in sim
class Object():
    
    def __init__(self, number, x, y, velocityx, velocityy, acceleration, radius, colour, collided):

        self.x = x # x position
        self.y = y # y position
        self.velx = velocityx # x velocity
        self.vely = velocityy # y velocity
        self.acc = acceleration # y acceleration
        self.colour = colour # colour of balls
        self.radius = radius # radius
        self.num = number # number identifier of ball
        self.KE = 0 # kinetic energy
        self.PE = 0 # potential energy
        self.collided = collided
    
    # updating position
    def posupdate(self):

        # timestep multiplication
        self.x += self.velx * dt
        self.y += self.vely * dt

        # updating potential energy (trying to keep proportional to kinetic energy)
        self.PE = 1/2 * (-1 * self.y + height - self.radius) ** 2
    
    # updating velocity
    def velupdate(self):

        # timestep multiplication
        self.vely += self.acc * dt

        # kinetic energy update
        self.KE = 1/2 * (self.velx**2 + self.vely**2)

        # checking for floor to bounce
        if self.y >= height - self.radius:

            self.vely = self.vely * -1 * damping # velocity becomes opposite

        # checking for sides to bounce
        elif self.x <= 0 + self.radius:
            self.velx = self.velx * -1 * damping

        elif self.x >= width - self.radius:
            self.velx = self.velx * -1 * damping

        else:
            pass

    # basic collision detection
    def collision(self, number, balllist):

        # iterate through the balls
        for k in range(0,ballmax):

            # not checking itself
            if number == k:
                pass
            
            elif self.collided == False:
                self.collided = True
                # the x and y radius of ball and the rest
                [xd, yd] = self.x - balllist[k].x, self.y - balllist[k].y

                # checking if any balls are withing the radius
                if ((xd)**2 + (yd)**2)**0.5 <= 2*self.radius:
                    
                    # finding angle between balls
                    if abs(xd) != 0:
                        theta = math.atan(abs(yd) / abs(xd))
                    else:
                        theta = math.atan(abs(yd) / (abs(xd) + 0.001))
                    
                    velmag = (self.velx**2 + self.vely**2)**0.5
                    print(velmag)


                    # checking angle
                    print(f" theta: {round(180/math.pi*theta,3)}")

                    # velocities should be opposite each other
                    self.velx = -(velmag*math.cos(theta))
                    self.vely = -(velmag*math.sin(theta))
                    balllist[k].velx = -(velmag*math.cos(theta))
                    balllist[k].vely = -(velmag*math.sin(theta))
                else:
                    pass
            else:
                pass
    # display information on the object for testing
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

# main function
def main():

    #pygame initialization
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('kinematic simulation')


    # testing variables
    vel = [40,-40]
    posx = [100,800]
    posy = [380,420]

    # instantiating balls in a range with random red colour
    for i in range(0,ballmax):
        balllist[i] = (Object(i, posx[i], posy[i], vel[i], 0, 0, 50, (random.randint(0,255),0,0), False))

    # main loop
    running = True
    while running:

        # quit on escape
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # quitting on escape key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # main clock for the simulation
        clock.tick(240)

        # fill screen (deleting old instances of objects)
        screen.fill((255,255,255))

        # update loop
        for i in range(0,ballmax):
            
            # drawing circles
            pygame.draw.rect(screen, (balllist[i].colour), (round(balllist[i].x - 1/2*balllist[i].radius), round(balllist[i].y - 1/2*balllist[i].radius), balllist[i].radius, balllist[i].radius))

            # updating the different variables
            balllist[i].posupdate()
            balllist[i].velupdate()
            balllist[i].collision(i, balllist)
        
        pygame.display.update()

main()
