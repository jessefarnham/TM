import enum

CONF_DIR = '../../conf'


class Terrain(enum.Enum):
    PLAINS = 0
    SWAMP = 1
    LAKE = 2
    FOREST = 3
    MOUNTAINS = 4
    WASTELAND = 5
    DESERT = 6
    RIVER = 7

    def to_texture(self):
        return self.name


class Element(enum.Enum):
    FIRE = 0
    WATER = 1
    EARTH = 2
    AIR = 3

    def to_texture(self):
        return self.name


class Direction(enum.Enum):
    NE = 30
    E = 90
    SE = 150
    SW = 210
    W = 270
    NW = 330


POWER_TEXTURE = "POWER"
TOWN_KEY_TEXTURE = "POWER"
