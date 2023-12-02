import random, pygame, pygame.gfxdraw

# default ball variables
colour = (0,0,0)


# pygame variables
width = 501
height = 701




def main():

    l = 1
    # main variables
    xCoordinate = 250
    yCoordinate = 300
    dt = 0.1
    acceleration = 10
    velocity = 20

    #pygame initialization
    pygame.init()

    clock = pygame.time.Clock()

    background_colour = (224, 225, 221)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('9 ball')
    screen.fill((255,255,255))


    # main loop
    running = True
    while running:

        # quit on escape
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # main clock for the simulation
        clock.tick(60)

        screen.fill((255,255,255))

        # draw ball on respective coordinate
        pygame.gfxdraw.filled_circle(screen, round(xCoordinate), round(yCoordinate), 15, colour)
        


        yCoordinate += velocity*dt


        if yCoordinate >= l + 100:
            velocity = -300
        elif yCoordinate <= 500 * l:
            velocity = 300
        else:
            pass
            
        l * 0.99
            
    
        pygame.display.update()

main()
