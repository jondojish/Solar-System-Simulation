# Example file showing a basic pygame "game loop"
import pygame
from physics import Vector, Body
from random import randint

# pygame setup
pygame.init()
WIDTH, HEIGHT = 1280, 720
HEIGHT_METRES = 20
RATIO = HEIGHT / HEIGHT_METRES
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
FPS = 120
GAME_FONT = pygame.freetype.SysFont("monospace", 24)

dt = 1 / FPS

ZOOM_FACTOR = 1.2
Body.set_metres_per_pixel(10**9)
sun = Body(radius=7*10**9.5, mass=1.989*10**30, vel=Vector(0, 0), pos=Vector(WIDTH*0.5, HEIGHT*0.5), color="yellow")
jupiter = Body(radius=7*10**9.5,mass=1.898*10**27, pos=Vector(WIDTH*0.5, sun.pos.y + 7.779 * 10**11), vel=Vector(13*10**3, 0), color="red")
jupiter.vel = Vector(0,0)
# earth = Body(radius=7*10**9.5, mass=6*10**26, vel=Vector(30 * 10**3, 0), pos=Vector(WIDTH * 0.25, sun.pos.y - 1.5 * 10**11), color="blue")

# used to put all bodies in correct positions on display
anchor_body = Body.bodies[0]
anchor_body.display_pos = Vector(WIDTH/2, HEIGHT/2)
for body in Body.bodies:
    body.display_pos = Vector.sum(anchor_body.display_pos, Vector.sum(body.pos, anchor_body.pos).multiply(1 / Body.metres_per_pixel))


w_down = False
s_down = False
a_down = False
d_down = False
drag = False
time_multiplier = 1
multiplier_base = 2
time_elapsed = 0
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # handles draging screen
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drag = True
        elif event.type == pygame.MOUSEMOTION and drag:
           rel_x, rel_y = event.rel
           for body in Body.bodies:
               body.display_pos.add(Vector(rel_x, rel_y))
        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False

    # handle zoom and time controls
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        time_multiplier = 0
    if keys[pygame.K_w] and w_down == False:
        Body.set_metres_per_pixel(Body.metres_per_pixel / ZOOM_FACTOR)
        for body in Body.bodies:
            centre_to_body = Vector.sum(body.display_pos, Vector(WIDTH/2, HEIGHT/2).negative())
            body.display_pos = Vector.sum(Vector(WIDTH/2, HEIGHT/2), centre_to_body.multiply(ZOOM_FACTOR))
        w_down = True
    elif not keys[pygame.K_w]:
        w_down = False
    if keys[pygame.K_s] and s_down == False:
        Body.set_metres_per_pixel(Body.metres_per_pixel * ZOOM_FACTOR)
        for body in Body.bodies:
            centre_to_body = Vector.sum(body.display_pos, Vector(WIDTH/2, HEIGHT/2).negative())
            body.display_pos = Vector.sum(Vector(WIDTH/2, HEIGHT/2), centre_to_body.multiply( 1/ZOOM_FACTOR))
        s_down = True
    elif not keys[pygame.K_s]:
        s_down = False
    if keys[pygame.K_d] and d_down == False:
        # time_multiplier *= 3
        time_multiplier += 1
        d_down = True
    elif not keys[pygame.K_d]:
        d_down = False
    if keys[pygame.K_a] and a_down == False:
        # time_multiplier /= 3
        time_multiplier -= 1
        a_down = True
    elif not keys[pygame.K_a]:
        a_down = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME
    if time_multiplier > 0:
        Body.update(dt*multiplier_base**(time_multiplier-1))
        time_elapsed += dt*multiplier_base**(time_multiplier-1)
        displayed_multiplier = multiplier_base**(time_multiplier-1)
    elif time_multiplier < 0:
        Body.update(-dt*multiplier_base**abs(time_multiplier))
        time_elapsed -= dt*multiplier_base**abs(time_multiplier+1)
        displayed_multiplier = -multiplier_base**abs(time_multiplier+1)
    elif time_multiplier == 0:
        displayed_multiplier = 0

    # time_elapsed += dt*time_multiplier
    GAME_FONT.render_to(screen, (0, 0), f"{int(time_elapsed)} secs | {round(time_elapsed / 31556952, 1)} years | x {displayed_multiplier}", (255, 255, 255))
    
    for body in Body.bodies:
        pygame.draw.circle(screen, body.color, body.display_pos.get_tuple(), body.radius / Body.metres_per_pixel)

    # flip() the display to put youwssswwr work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(FPS) / 1000
    pygame.event.pump() 

pygame.quit()
