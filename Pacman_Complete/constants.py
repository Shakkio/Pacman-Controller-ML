from vector import Vector2

TILEWIDTH = 16
TILEHEIGHT = 16
NROWS = 36
NCOLS = 28
SCREENWIDTH = NCOLS*TILEWIDTH
SCREENHEIGHT = NROWS*TILEHEIGHT
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255,100,150)
TEAL = (100,255,255)
ORANGE = (230,190,40)
GREEN = (0, 255, 0)

STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
PORTAL = 3

PACMAN = 0
PELLET = 1
POWERPELLET = 2
GHOST = 3
BLINKY = 4
PINKY = 5
INKY = 6
CLYDE = 7
FRUIT = 8

SCATTER = 0
CHASE = 1
FREIGHT = 2
SPAWN = 3

SCORETXT = 0
LEVELTXT = 1
READYTXT = 2
PAUSETXT = 3
GAMEOVERTXT = 4

# how often the algorithm will take a random action, rather than the best action it knows so far.
RHO = 0.2

# how much an action’s Q-value depends on the Q-value at the state (or states) it leads to.
GAMMA = 0.9

# controls how much influence the current feedback value has over the stored Q-value.
ALPHA = 0.9

# number of iterations
ITERATIONNUMBER = 40000
# length of sequence or walk
NU = 0.05


NODE_POSITIONS_IGNORE = [
  Vector2(184.0, 256.0),
  Vector2(184.0, 272.0),
  Vector2(184.0, 288.0),
  Vector2(248.0, 256.0),
  Vector2(248.0, 288.0),
  Vector2(248.0, 272.0),
  Vector2(216.0, 272.0),
  Vector2(144.0, 224.0),
  Vector2(240.0, 224.0),
  Vector2(288.0, 224.0),
  Vector2(144.0, 272.0),
  Vector2(144.0, 320.0),
  Vector2(192.0, 224.0),
  Vector2(288.0, 272.0),
  Vector2(288.0, 320.0),
  Vector2(432.0, 272.0),
  Vector2(0.0, 272.0),
  Vector2(216.0, 224.0)
]
