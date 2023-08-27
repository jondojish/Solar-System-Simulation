# Example file showing a basic pygame "game loop"
import pygame
import json
import os
from physics import Vector, Body
from datetime import datetime
from data import get_data

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
TIME_UNIT_MULTIPLIER = 100

dt = 1 / FPS

ZOOM_FACTOR = 1.2
earth_radius = 10**3 * 6.371*10**6
earth_mass = 5.9722*10**24
Body.set_metres_per_pixel(10**9)
sun = Body(radius=5 * earth_radius, mass=1988500*10**24, vel=Vector(0, 0), pos=Vector(WIDTH*0.5, HEIGHT*0.5), color="yellow")
sun.name = "sun"
date = datetime.today()

planets = ["mercury", "venus", "earth", "moon", "mars", "jupiter", "saturn", "neptune", "uranus"]
generation = {"mercury": {"radius": 0.383, "mass": 0.0553, "color": "purple"}, 
              "venus": {"radius": 0.950, "mass": 0.815, "color": "white"}, 
              "earth": {"radius": 1, "mass": 1, "color": "green"}, 
              "moon": {"radius": 0.2727, "mass": 0.0123, "color": "grey"},
              "mars": {"radius": 0.532, "mass": 0.107, "color": "red"},
              "jupiter": {"radius": 10.973, "mass": 317.83, "color": "brown"},
              "saturn": {"radius": 9.140, "mass": 95.16, "color": "brown"},
              "neptune": {"radius": 3.865, "mass": 17.15, "color": "white"},
              "uranus": {"radius": 3.929, "mass": 14.54, "color": "white"}}

data_to_write = {}
with open("data.json", "r") as f:
    if os.stat("data.json").st_size != 0:
        data = json.load(f)
    else: data = {}
    if data.get("date") ==  datetime.today().strftime("%Y-%m-%d"):
        for planet in planets:
            vel = Vector(data[planet]["vel"][0], data[planet]["vel"][1])
            pos = Vector(data[planet]["pos"][0], data[planet]["pos"][1])
            radius = generation[planet]["radius"]
            mass = generation[planet]["mass"]
            color = generation[planet]["color"]
            if planet == "moon":
                body = Body(radius=radius * earth_radius, mass=mass * earth_mass, vel=Vector.sum(Body.get_by_name("earth").vel, vel), pos=Vector.sum(Body.get_by_name("earth").pos, pos), color=color)
            else:
                body = Body(radius=radius * earth_radius, mass=mass * earth_mass, vel=vel, pos=Vector.sum(sun.pos, pos), color=color)
            body.name = planet
    else:
        data_to_write = {"date": datetime.today().strftime("%Y-%m-%d")}
        for planet in planets:
            data = get_data(planet, date)
            vel = Vector(data["vel"][0], data["vel"][1])
            pos = Vector(data["pos"][0], data["pos"][1])
            data_to_write[planet] = data
            radius = generation[planet]["radius"]
            mass = generation[planet]["mass"]
            color = generation[planet]["color"]
            if planet == "moon":
                body = Body(radius=radius * earth_radius, mass=mass * earth_mass, vel=Vector.sum(Body.get_by_name("earth").vel, vel), pos=Vector.sum(Body.get_by_name("earth").pos, pos), color=color)
            else:
                body = Body(radius=radius * earth_radius, mass=mass * earth_mass, vel=vel, pos=Vector.sum(sun.pos, pos), color=color)
            body.name = planet
if data_to_write != {}:
    with open("data.json", "w") as f:
        f.write(json.dumps(data_to_write))

# used to test accuracy
# earth_test = Body(radius=earth_radius, mass=0, vel=Vector(0, 0), pos=Vector.sum(sun.pos, Vector.sum(Body.get_by_name("earth").pos, Vector(1, 1))), color="orange")


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
time_rewind = False
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
        time_multiplier += 3
        d_down = True
    elif not keys[pygame.K_d]:
        d_down = False
    if keys[pygame.K_a] and a_down == False:
        time_multiplier -= 3
        a_down = True
    elif not keys[pygame.K_a]:
        a_down = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME
    if time_multiplier > 0:
        # Body.update(dt*multiplier_base**(time_multiplier-1))
        displayed_multiplier = multiplier_base**(time_multiplier-1)
        # using dynamic units so that perfomance is constant accross all play speeds
        Body.update_all(dt*displayed_multiplier, dt*displayed_multiplier / TIME_UNIT_MULTIPLIER)
        time_elapsed += dt*multiplier_base**(time_multiplier-1)
    else:
        time_multiplier = 0
        displayed_multiplier = 0

    GAME_FONT.render_to(screen, (0, 0), f"{int(time_elapsed)} secs | {round(time_elapsed / 31556952, 1)} years | x {displayed_multiplier} | {int(1 /dt)} FPS", (255, 255, 255))


    for body in Body.bodies:
        pygame.draw.circle(screen, body.color, body.display_pos.get_tuple(), body.radius / Body.metres_per_pixel)
        if Vector.sum(body.display_pos, Body.get_by_name("sun").display_pos.negative()).get_magnitude() > WIDTH * 0.023 or body.name == "sun":
            GAME_FONT.render_to(screen, (body.display_pos.x - body.radius / Body.metres_per_pixel, body.display_pos.y + body.radius / Body.metres_per_pixel), f"{body.name}", (255, 255, 255))

    # flip() the display to put youwssswwr work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(FPS) / 1000
    pygame.event.pump() 

pygame.quit()
