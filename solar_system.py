import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

pygame.init()
display = pygame.display.list_modes()[0]  # Get the current screen resolution
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
pygame.display.set_caption("Solar System Simulation")
pygame.mouse.set_visible(False)

# Try to load background music
try:
    pygame.mixer.init()
    pygame.mixer.music.load("space-rumble-29970.mp3")
    pygame.mixer.music.play(-1)
except:
    print("Could not load music.")

# Set up perspective and initial camera
gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)  # Allow glColor to affect material

# Set up lighting
glLightfv(GL_LIGHT0, GL_POSITION, (10, 5, 10, 0))  # Directional light
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))  # Softer ambient
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.7, 0.7, 0.7, 1))  # Balanced diffuse
glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 1))  # Reduced specular

# Set up perspective and initial camera
gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

# Set up lighting
glLightfv(GL_LIGHT0, GL_POSITION, (10, 5, 10, 0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.7, 0.7, 0.7, 1))
glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 1))

# Sun, planet, and moon data
planets = [
    {"name": "Sun", "radius": 2.0, "distance": 0, "speed": 0, "color": (1, 1, 0), "moons": []},
    {"name": "Mercury", "radius": 0.2, "distance": 4, "speed": 0.03, "color": (0.5, 0.5, 0.5), "moons": []},
    {"name": "Venus", "radius": 0.3, "distance": 5.5, "speed": 0.025, "color": (1, 0.8, 0.2), "moons": []},
    {"name": "Earth", "radius": 0.5, "distance": 7, "speed": 0.02, "color": (0, 0.5, 1), "moons": [
        {"radius": 0.1, "distance": 0.8, "speed": 0.1, "color": (0.7, 0.7, 0.7)}
    ]},
    {"name": "Mars", "radius": 0.4, "distance": 9, "speed": 0.018, "color": (1, 0.3, 0), "moons": [
        {"radius": 0.05, "distance": 0.6, "speed": 0.12, "color": (0.6, 0.6, 0.6)},
        {"radius": 0.05, "distance": 0.8, "speed": 0.1, "color": (0.6, 0.6, 0.6)}
    ]},
    {"name": "Jupiter", "radius": 1.0, "distance": 12, "speed": 0.012, "color": (1, 0.6, 0.2), "moons": [
        {"radius": 0.15, "distance": 1.5, "speed": 0.08, "color": (0.8, 0.7, 0.6)},
        {"radius": 0.12, "distance": 1.8, "speed": 0.07, "color": (0.8, 0.7, 0.6)},
        {"radius": 0.1, "distance": 2.0, "speed": 0.06, "color": (0.8, 0.7, 0.6)},
        {"radius": 0.1, "distance": 2.2, "speed": 0.05, "color": (0.8, 0.7, 0.6)}
    ]},
    {"name": "Saturn", "radius": 0.9, "distance": 16, "speed": 0.009, "color": (1, 1, 0.5), "moons": [
        {"radius": 0.12, "distance": 1.5, "speed": 0.07, "color": (0.7, 0.7, 0.6)},
        {"radius": 0.1, "distance": 1.8, "speed": 0.06, "color": (0.7, 0.7, 0.6)},
        {"radius": 0.08, "distance": 2.0, "speed": 0.05, "color": (0.7, 0.7, 0.6)}
    ]},
    {"name": "Uranus", "radius": 0.7, "distance": 20, "speed": 0.006, "color": (0.5, 1, 1), "moons": []},
    {"name": "Neptune", "radius": 0.7, "distance": 24, "speed": 0.004, "color": (0.3, 0.5, 1), "moons": []},
]

# # Planet angle state
# angles = [0 for _ in planets]

# # Camera control variables
# camera_rot_x = 0
# camera_rot_y = 0
# camera_distance = 40
# last_mouse_pos = None

# Asteroid belt
num_asteroids = 100
asteroids = [
    {
        "radius": random.uniform(0.05, 0.1),
        "distance": random.uniform(10, 11),
        "speed": random.uniform(0.01, 0.015),
        "color": (random.uniform(0.4, 0.6), random.uniform(0.4, 0.6), random.uniform(0.4, 0.6)),
        "angle": random.uniform(0, 2 * math.pi)
    }
    for _ in range(num_asteroids)
]


# Planet and asteroid angle state
planet_angles = [0 for _ in planets]
asteroid_angles = [a["angle"] for a in asteroids]
moon_angles = [[0 for _ in p["moons"]] for p in planets]

# Camera control variables
camera_rot_x = 0
camera_rot_y = 0
camera_distance = 40
last_mouse_pos = None


# Draw a sphere with proper color application
def draw_sphere(radius, color, texture_id=None):
    glColor3fv(color)
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.5, 0.5, 0.5, 1))
    glMaterialfv(GL_FRONT, GL_SHININESS, 20)
    
    quadric = gluNewQuadric()
    if texture_id:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, 32, 16)
    if texture_id:
        glDisable(GL_TEXTURE_2D)
    gluDeleteQuadric(quadric)

# Draw orbital path
def draw_orbit(distance):
    glDisable(GL_LIGHTING)
    glColor3f(0.3, 0.3, 0.3)  # Faint gray orbit
    glBegin(GL_LINE_LOOP)
    for i in range(100):
        theta = i * 2 * math.pi / 100
        x = distance * math.cos(theta)
        z = distance * math.sin(theta)
        glVertex3f(x, 0, z)
    glEnd()
    glEnable(GL_LIGHTING)

# Comet class with trail effect
class Comet:
    def __init__(self):
        self.trail = []
        self.trail_length = 20
        self.reset()

    def reset(self):
        self.x = random.uniform(-100, 100)
        self.y = random.uniform(-50, 50)
        self.z = random.uniform(-100, -50)
        self.dx = random.uniform(-0.2, 0.2)
        self.dy = random.uniform(-0.2, 0.2)
        self.dz = random.uniform(0.1, 0.4)
        self.trail = []

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        self.trail.append((self.x, self.y, self.z))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        if abs(self.x) > 150 or abs(self.y) > 100 or self.z > 50:
            self.reset()

    def draw(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINE_STRIP)
        for i, pos in enumerate(self.trail):
            alpha = i / self.trail_length
            glColor4f(1, 1, 1, alpha)
            glVertex3f(*pos)
        glEnd()
        glEnable(GL_LIGHTING)

        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        draw_sphere(0.2, (1, 1, 1))
        glPopMatrix()

comets = [Comet() for _ in range(3)]


# Star field for skybox with movement
num_stars = 1000
star_positions = []
star_velocities = []
skybox_radius = 100
for _ in range(num_stars):
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    star_positions.append([theta, phi])
    # Reduced angular velocities for slower twinkling
    star_velocities.append([random.uniform(-0.0001, 0.0001), random.uniform(-0.0001, 0.0001)])
    
    
# OpenGL error checking
def check_opengl_error():
    error = glGetError()
    if error != GL_NO_ERROR:
        print("OpenGL error:", gluErrorString(error))



clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                camera_distance = max(10, camera_distance - 2)
            elif event.button == 5:  # Scroll down
                camera_distance = min(60, camera_distance + 2)
        elif event.type == MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            if last_mouse_pos:
                dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                camera_rot_y += dx * 0.2
                camera_rot_x = max(-90, min(90, camera_rot_x + dy * 0.2))
            last_mouse_pos = event.pos
        elif event.type == MOUSEBUTTONUP:
            last_mouse_pos = None

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up camera
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
    glTranslatef(0, 0, -camera_distance)
    glRotatef(camera_rot_x, 1, 0, 0)
    glRotatef(camera_rot_y, 0, 1, 0)

    # Update star positions for twinkling
    for i in range(num_stars):
        theta, phi = star_positions[i]
        dtheta, dphi = star_velocities[i]
        theta += dtheta
        phi += dphi
        phi = max(0, min(math.pi, phi))
        theta = theta % (2 * math.pi)
        star_positions[i] = [theta, phi]

    # Draw stars (skybox effect)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)
    for theta, phi in star_positions:
        x = skybox_radius * math.sin(phi) * math.cos(theta)
        y = skybox_radius * math.sin(phi) * math.sin(theta)
        z = skybox_radius * math.cos(phi)
        glVertex3f(x, y, z)
    glEnd()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    # Draw orbital paths for planets
    for p in planets[1:]:  # Skip Sun
        draw_orbit(p["distance"])

    # Draw Sun, planets, and moons
    for i, p in enumerate(planets):
        glPushMatrix()
        if i != 0:  # Planets orbit the Sun
            planet_angles[i] += p["speed"]
            x = math.cos(planet_angles[i]) * p["distance"]
            z = math.sin(planet_angles[i]) * p["distance"]
            glTranslatef(x, 0, z)
        draw_sphere(p["radius"], p["color"])

        # Draw moons
        for j, moon in enumerate(p["moons"]):
            glPushMatrix()
            moon_angles[i][j] += moon["speed"]
            mx = math.cos(moon_angles[i][j]) * moon["distance"]
            mz = math.sin(moon_angles[i][j]) * moon["distance"]
            glTranslatef(mx, 0, mz)
            draw_sphere(moon["radius"], moon["color"])
            glPopMatrix()

        glPopMatrix()

    # Draw asteroids
    for i, a in enumerate(asteroids):
        glPushMatrix()
        asteroid_angles[i] += a["speed"]
        x = math.cos(asteroid_angles[i]) * a["distance"]
        z = math.sin(asteroid_angles[i]) * a["distance"]
        glTranslatef(x, 0, z)
        draw_sphere(a["radius"], a["color"])
        glPopMatrix()

    # Draw comets
    for comet in comets:
        comet.update()
        comet.draw()

    check_opengl_error()
    pygame.display.flip()
    clock.tick(60)