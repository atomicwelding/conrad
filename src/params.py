GAME_TITLE = 'conrad'

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 768

ASSETS_PATH = 'assets'
BACKGROUND_PATH = 'green_bg.png'


NB_HEAVY_MISSILE = 2
NB_LIGHT_MISSILE = 2

# physical constants
G = 6.67*10e-11
c = 1
R_S = 100

# scaling factors
alpha = 10e-18
beta = 10e-1
gamma = 10e-2

# physical quantities
M = 1/(2*G) 
m = alpha * M
mu = M*G

RESTITUTION = 1

def radial_acc(entity):
    a = ( - G*M/entity.rr**2 )
    b = (entity.rr - 3/2 * R_S) * (entity.l0**2)/(entity.rr**4)

    return a + b 

# physical integration 
dt = 0.01
T = 4
nb_steps = int(T / dt)
