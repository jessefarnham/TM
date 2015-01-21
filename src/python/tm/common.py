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