# standard libraries 
import random
import math

# third party libraries
import pygame, pygame.gfxdraw
import numpy as np

# simulation variables
DT = 0.1 # timestep
DAMPING = 1 # damping due to loss of energy, not working
WINDOW_WIDTH = 1001 # window width dimension
WINDOW_HEIGHT = 701 # window height dimension
BALL_AMOUNT = 20 # amount of balls
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
        self.momentum = self.radius * self.total_velocity
    
    # updating velocity
    def update_velocity(self):

        # updating the velocity based on the acceleration
        self.velx += self.accx * DT
        self.vely += self.accy * DT

        # kinetic energy update
        self.KE = (0.5 * (self.total_velocity ** 2))

    def update_collision(self, number, ball_list, screen):

        # checking for floor to bounce
        if self.y >= WINDOW_HEIGHT - self.radius:

            self.vely = -1 * self.vely * DAMPING # velocity becomes opposite
            self.y += WINDOW_HEIGHT - (self.y + self.radius) # moving position slightly to not clip inside

        elif self.y <= self.radius:

            self.vely = -1 * self.vely * DAMPING # velocity becomes opposite
            self.y -= (self.y - self.radius) # moving position slightly to not clip inside

        # checking for sides to bounce
        elif self.x <= self.radius:

            self.velx = -1 * self.velx * DAMPING # velocity becomes opposite
            self.x -= (self.x - self.radius) # moving position slightly to not clip inside

        elif self.x >= WINDOW_WIDTH - self.radius:
            
            self.velx = -1 * self.velx * DAMPING # velocity becomes opposite
            self.x += WINDOW_WIDTH - (self.x + self.radius) # moving position slightly to not clip inside
        
        for k in range(0,BALL_AMOUNT):

            # difference in positions of two balls
            delta_x = self.x - ball_list[k].x
            delta_y = self.y - ball_list[k].y
            delta_radius = self.radius + BALL_LIST[k].radius
            
            # overlap between the two balls
            collision_overlap = ((delta_x**2+delta_y**2)**0.5) - (delta_radius)

            # not checking itself
            if number == k:
                pass
            
            else:
                if ((delta_x)**2 + (delta_y)**2)**0.5 <= delta_radius:

                    # normal vector between going from one ball to other
                    collision_normal = np.array([delta_x,delta_y])

                    # unit vector of collision normal
                    rotation_matrix = np.array([[0,1],[-1,0]])
                    unit_vector = 1/((delta_x**2+delta_y**2)**0.5)*collision_normal
                    unit_vector_orthag = unit_vector@rotation_matrix
                    projection_normal_orthag = ((np.dot(collision_normal, unit_vector_orthag))/np.linalg.norm(unit_vector_orthag)**2)*unit_vector_orthag
                    #pygame.draw.line(screen, (255,255,255), (self.x - delta_x/2, self.y - delta_y/2),(100*unit_vector_orthag[0]+self.x - delta_x/2, 100*unit_vector_orthag[1] + self.y - delta_y/2), 2)
                    #pygame.draw.line(screen, (255,255,255), (ball_list[k].x + delta_x/2, ball_list[k].y - delta_y/2), (0,1), 3)

                    # spacing the balls apart
                    self.x += collision_overlap*unit_vector[0]/2
                    self.y += collision_overlap*unit_vector[1]/2
                    ball_list[k].x += collision_overlap*unit_vector[0]/2
                    ball_list[k].y += collision_overlap*unit_vector[1]/2

                    # updating self velocity
                    self.velx = unit_vector[0]*self.total_velocity*DAMPING
                    self.vely = unit_vector[1]*self.total_velocity*DAMPING

                    # updating the colliding balls velocity
                    ball_list[k].vely = -1*unit_vector_orthag[0]*ball_list[k].total_velocity*DAMPING
                    ball_list[k].vely = -1*unit_vector_orthag[1]*ball_list[k].total_velocity*DAMPING

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
            accelerationx: {self.accx}
            accelerationy: {self.accy}
                """)

def main():

    # pygame initialization
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('kinematic simulation')


    # testing variables
    vel = [10,-10]
    posx = [400,500]
    posy = [400 + 25,400 - 25]
    colours = []
    for i in range(0,BALL_AMOUNT):
        x = (random.randint(0,255),random.randint(0,255),0)
        colours.append(x)
        

    # instantiating balls in a range with random red colour
    for i in range(0,BALL_AMOUNT):
        #BALL_LIST[i] = (Ball(i, posx[i], posy[i], vel[i], 0, 0, 0, 50, (255,random.randint(0,255),0)))
        BALL_LIST[i] = (Ball(i,  random.randint(50, 900),  random.randint(50,500), random.randint(-20,20), 10, 0, 7, 20, colours[i]))

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
        clock.tick(60)

        # fill screen (deleting old instances of objects)
        screen.fill((10,10,10))

        # update loop
        for i in range(0,BALL_AMOUNT):
            
            # drawing circles
            pygame.gfxdraw.filled_circle(screen, round(BALL_LIST[i].x), round(BALL_LIST[i].y), BALL_LIST[i].radius, BALL_LIST[i].colour)
            
            # updating the different variables
            BALL_LIST[i].update_collision(BALL_LIST[i].num, BALL_LIST, screen)
            BALL_LIST[i].update_position()
            BALL_LIST[i].update_velocity()
            
        
        pygame.display.update()

main()
