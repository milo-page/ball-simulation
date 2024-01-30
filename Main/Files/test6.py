# standard library imports
import random, math

# third-party imports
import pygame, pygame.gfxdraw
import numpy as np

# simulation constants
DT = 0.1 # timestep
DAMPING = 1# damping due to loss of energy, not working
WINDOW_WIDTH = 1001 # window width dimension
WINDOW_HEIGHT = 701 # window height dimension
BALL_AMOUNT = 10 # amount of balls
BALL_LIST = BALL_AMOUNT*[0] # empty list to contain ball objects

# class for balls in sim
class Ball():
    
    def __init__(self, number, x, y, velocityx, velocityy, accelerationx, accelerationy, radius, colour):

        self.x = x # x position
        self.y = y # y position
        self.velx = velocityx # x velocity
        self.vely = velocityy # y velocity
        self.accx = accelerationx # y acceleration
        self.accy = accelerationy # y acceleration
        self.colour = colour # colour of ball
        self.radius = radius # radius of ball
        self.num = number # number identifier
        self.KE = 0 # kinetic energy
        self.PE = 0 # potential energy
        self.momentum = 0 # initializaing momentum
        self.total_velocity = 0 # initializing the total velocity
    
    # updating position
    def update_position(self):

        # updating position based on velocity
        self.x += self.velx * DT
        self.y += self.vely * DT

        # updating potential energy (trying to keep proportional to kinetic energy)
        self.PE = (0.5 * ((-1 * self.y + WINDOW_HEIGHT - self.radius) ** 2))
        self.total_velocity = (self.velx**2 + self.vely**2)**0.5
        self.momentum = self.radius*self.total_velocity
    
    # updating velocity
    def update_velocity(self):

        # updating the velocity based on the acceleration
        self.velx += self.accx * DT
        self.vely += self.accy * DT

        # kinetic energy update
        self.KE = (0.5 * (self.total_velocity ** 2))

    def update_collision(self, number, ball_list):
        
        def ball_collision():
                
            for k in range(0,BALL_AMOUNT):

                # not checking itself
                if number == k:
                    pass
                
                else:
                    if ((self.y - BALL_LIST[k].y)**2 + (self.x - BALL_LIST[k].x)**2)**0.5 <= self.radius + BALL_LIST[k].radius:
                        
                        delta_x = self.x - ball_list[k].x
                        delta_y = self.y - ball_list[k].y

                        collision_vector = np.array([delta_x,delta_y])

                        unit_vector = 1/((delta_x**2+delta_y**2)**0.5)*collision_vector

                        self.velx = unit_vector[0]*ball_list[k].total_velocity*DAMPING
                        self.vely = unit_vector[1]*ball_list[k].total_velocity*DAMPING
                        ball_list[k].vely = -1*unit_vector[1]*self.total_velocity*DAMPING
                        ball_list[k].vely = -1*unit_vector[1]*self.total_velocity*DAMPING

        # checking for floor to bounce
        if self.y >= WINDOW_HEIGHT - self.radius or self.y <= self.radius:

            self.vely = -1 * self.vely * DAMPING # velocity becomes opposite

        # checking for sides to bounce
        elif self.x <= self.radius or self.x >= WINDOW_WIDTH - self.radius:
            
            self.velx = -1 * self.velx * DAMPING # velocity becomes opposite
        
        else:
            pass


        #ball_collision()

        
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

def main():

    # pygame initialization
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('kinematic simulation')


    # testing variables
    vel = [40,-40]
    posx = [100,901]
    posy = [400 - 25,400 + 25]

    # instantiating balls in a range with random red colour
    for i in range(0,BALL_AMOUNT):
        #BALL_LIST[i] = (Ball(i, posx[i], posy[i], vel[i], 0, 0, 10, 50, (random.randint(0,255),0,0)))
        BALL_LIST[i] = (Ball(i,  random.randint(100,500),  random.randint(100,500), random.randint(-20,20), random.randint(-20,20), 0, 0, 10, (random.randint(0,255),0,0)))

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
        clock.tick(120)

        # fill screen (deleting old instances of objects)
        screen.fill((255,255,255))

        # update loop
        for i in range(0,BALL_AMOUNT):
            
            # drawing circles
            pygame.gfxdraw.filled_circle(screen, round(BALL_LIST[i].x), round(BALL_LIST[i].y), BALL_LIST[i].radius, BALL_LIST[i].colour)
            
            # updating the different variables
            BALL_LIST[i].update_collision(BALL_LIST[i].num, BALL_LIST)
            BALL_LIST[i].update_position()
            BALL_LIST[i].update_velocity()
            
        
        pygame.display.update()

main()