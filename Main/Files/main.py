# standard library imports
import random, math

# third-party imports
import pygame
import pygame.gfxdraw
import numpy as np

# simulation constants
DT = 0.1 # timestep
DAMPING = 1 # damping due to loss of energy, not working
WINDOW_WIDTH = 1001 # window width dimension
WINDOW_HEIGHT = 701 # window height dimension
BALL_AMOUNT = 5 # amount of balls
BALL_LIST = BALL_AMOUNT*[0] # empty list to contain ball objects

def magnitude(x: np.array):

    return np.sqrt(np.dot(x, x))


# class for balls in simulation
class Ball():
    
    def __init__(self, number, position, velocity, acceleration, radius, colour):

        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration # acceleration
        self.colour = colour # colour of ball
        self.radius = radius # radius of ball
        self.num = number # number identifier
    
    # updating position
    def update_position(self):

        # updating position based on velocity
        self.position = np.add(self.position, self.velocity * DT)

        # momentum (using radius as mass)
        self.momentum = self.radius * magnitude(self.velocity)
    
    # updating velocity
    def update_velocity(self):

        # updating the velocity based on the acceleration
        self.velocity = np.add(self.velocity, self.acceleration * DT)

    def update_collision(self, ball_list):
        
        def ball_collision():
                
            for k in range(0, BALL_AMOUNT):

                # not checking itself
                if self.number == k:
                    pass
                
                # checking when ball is inside anothers radius
                # TODO optimize
                else:
                    delta_position = np.add(self.position, -ball_list[k].position)

                    if (magnitude(delta_position)) <= self.radius + ball_list[k].radius:
                        delta_position = np.add(self.position, -ball_list[k].position)

                        unit_vector = 1/(magnitude(delta_position)) * delta_position

                        self.velocity = unit_vector*magnitude(ball_list[k].velocity)*DAMPING
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


        ball_collision()

        
    # display information on the object for testing
    def display(self):
        print(f"""
            x: {self.x}
            y: {self.y}
            x velocity: {round(self.velx, 2)}
            y velocity: {round(self.vely, 2)}
            acceleration: {self.acc}
            """)

def main():

    # pygame initialization
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('kinematic simulation')

    # instantiating balls in a range with random red colour
    for i in range(0,BALL_AMOUNT):
        BALL_LIST[i] = (Ball(i,  np.array(random.randint(100,500)), np.array(random.randint(-11,11)), np.array((0,5)), 25, (random.randint(0,255),0,0)))

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