import random, pygame, pygame.gfxdraw, json

# default ball variables
colour = (0,0,0)


# pygame variables
width, height = (501, 701)

def main():

    # main variables
    xCoordinate = 250
    yCoordinate = 100
    dt = 0.1
    acceleration = 10
    velocity = 0

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
        

        KineticE = 1/2 * (velocity)**2
        PotentialE = 601 - yCoordinate
        TotalE = (abs(KineticE) + abs(1/2 * PotentialE))/10

        if KineticE + PotentialE > 0.1:
            yCoordinate += velocity*dt
            velocity += acceleration*dt

            if yCoordinate >= 685:
                #velocity = velocity*(-0.9)
                velocity = velocity*-0.9
                
            else:
                pass
        
        
            
            
            print(f"Kinetic Energy: {int(round(KineticE, 1))} Potential Energy: {int(round(PotentialE, 1))} ")
        else:
            pass
        
        pygame.draw.line(screen, (255,0,0), (5,701), (5, (701 - round((701/5832)*KineticE))), 10)
        pygame.draw.line(screen, (0,255,0), (16,701), (16, (701 - round((800/685)*PotentialE))), 10)
        pygame.draw.line(screen, (0,0,255), (27,701), (27, (701 - TotalE)), 10)

        pygame.display.update()

main()
