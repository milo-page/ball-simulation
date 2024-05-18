# standard library imports
import random, time

# third-party imports
import pygame
import pygame.gfxdraw
import numpy as np

# simulation constants
DT = 0.1 # timestep
DAMPING = 1# damping due to loss of energy, not working
WINDOW_WIDTH = 1001 # window width dimension
WINDOW_HEIGHT = 701 # window height dimension
BALL_AMOUNT = 2 # amount of balls
BALL_LIST = BALL_AMOUNT*[0] # empty list to contain ball objects

def magnitude(x: np.array):

    return np.sqrt(np.dot(x, x))


# class for balls in sim
class Ball():
    
    def __init__(self,
                number: int,
                position: np.array,
                velocity: np.array,
                acceleration: np.array,
                radius: int,
                colour: tuple[int, int, int]):
        
        self.number = number # number identifier
        self.position = position # position the ball is currently
        self.velocity = velocity # velocity
        self.acceleration = acceleration # acceleration
        self.colour = colour # colour of ball
        self.radius = radius # radius of ball
        self.mass = radius # future feature
        
    
    # updating position
    def update_position(self):

        # updating position based on velocity
        self.position = np.add(self.position, self.velocity * DT)

        # momentum
        self.momentum = self.mass * self.velocity
    
    # updating velocity
    def update_velocity(self):

        # updating the velocity based on the acceleration
        self.velocity = np.add(self.velocity, self.acceleration * DT)

    
    def update_collision(self, number, ball_list):
        
        def ball_collision():
                
            for k in range(0,BALL_AMOUNT):

                # not checking itself
                
                if number == k:
                    pass
                
                # checking when ball is inside anothers radius
                else:
                    
                    # TODO make it only check balls that havent been checked (n^2 -> n!)
                    # would have to redo because now it uses this fact to calculate for both
                    delta_position = np.add(self.position, - ball_list[k].position)
                    min_radius = self.radius + ball_list[k].radius
                    if self.number == 0:
                        print(f"difference in position: {delta_position}")

                    if magnitude(delta_position) < min_radius:
                        
                        a = self.mass
                        b = ball_list[k].mass
                        def f(x, y): return (x - y)/(x + y)
                        def g(x, y): return (2 * y)/(x + y)
                        

                        # collison precion eg. moving them outside of each other
                        
                        collision_unit_vector = delta_position * (1 / magnitude(delta_position))
                        overlap = (min_radius - magnitude(delta_position)) / 2
                        collision_vector = overlap * collision_unit_vector
                        self.position = np.add(self.position, collision_vector)
                        ball_list[k].position = np.add(ball_list[k].position, -collision_vector)


                        #self.velocity = np.add((f(a, b) * self.velocity), (g(a, b) * ball_list[k].velocity))
                        #self.velocity = self.velocity * -1
                        #ball_list[k].velocity = ball_list[k].velocity * -1

                        self.velocity = 40 * collision_vector

                        print("collided: ", magnitude(delta_position) < min_radius)
                        print(f"collision vector {collision_vector} of ball {self.number}")
                        ball_list[k].velocity = 40 * -collision_vector
                        
                        #ball_list[k].velocity = np.add((f(b, a) * ball_list[k].velocity), (g(b, a) * self.velocity))
                        #self.velocity = self.velocity * -1
                        #ball_list[k].velocity = ball_list[k].velocity * -1
                        #self.velocity = np.array((0, 0))
                        #ball_list[k].velocity = np.array((0, 0))

                        """unit_vector = 1/(magnitude(delta_position)) * delta_position

                        self.velocity = unit_vector*magnitude(ball_list[k].velocity)*DAMPING
                        self.vely = unit_vector[1]*ball_list[k].total_velocity*DAMPING
                        ball_list[k].vely = -1*unit_vector[1]*self.total_velocity*DAMPING
                        ball_list[k].vely = -1*unit_vector[1]*self.total_velocity*DAMPING"""

        # checking for floor to bounce
        # TODO optimize with vectors
        if self.position[1] >= WINDOW_HEIGHT - self.radius or self.position[1] <= self.radius:

            self.velocity[1] = -1 * self.velocity[1] * DAMPING # velocity becomes opposite

        # checking for sides to bounce
        elif self.position[0] <= self.radius or self.position[0] >= WINDOW_WIDTH - self.radius:
            
            self.velocity[0] = -1 * self.velocity[0] * DAMPING # velocity becomes opposite
        
        else:
            pass


        ball_collision()

def main():

    # pygame initialization
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('kinematic simulation')

    # instantiating balls in a range with random red colour
    pos = [300, 590]
    pos2 = [300, 315]
    vel = [40, -40]
    colours = [0, 255]
    for i in range(0,BALL_AMOUNT):
        BALL_LIST[i] = (Ball(i, np.array([pos[i], pos2[i]]), np.array([vel[i], 0]), np.array([0, 10]), 25, (colours[i],0,0)))

    # main loop
    running = True
    run = False
    while running:

        tick = False


        # quit on escape
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # quitting on escape key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
                elif event.key == pygame.K_SPACE:
                    tick = True

                elif event.key == pygame.K_r:
                    run = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            tick = True

        # main clock for the simulation
        if run == True:
            clock.tick(60)

        # fill screen (deleting old instances of objects)
        screen.fill((255,255,255))
        
        
        # update loop
        for i in range(0,BALL_AMOUNT):
            
            # drawing circles
            pygame.gfxdraw.filled_circle(screen, round(BALL_LIST[i].position[0]), round(BALL_LIST[i].position[1]), BALL_LIST[i].radius, BALL_LIST[i].colour)
            
            if tick == True or run == True:

                # updating the different variables
                BALL_LIST[i].update_collision(BALL_LIST[i].number, BALL_LIST)
                BALL_LIST[i].update_position()
                BALL_LIST[i].update_velocity()
                
        
        pygame.display.update()

main()