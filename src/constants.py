from enum import IntEnum, auto, Enum
from src.util import Vec

WIDTH, HEIGHT = 1280, 768 # pixels
SIZE = Vec(WIDTH, HEIGHT) # pixels

class Layer(Enum):
    BG = auto()
    MG = auto()
    PLAYER = auto()
    FG = auto()
    CROSSHAIR = auto()
    DEBUG = auto()
    HUD = auto()

BLOCK = 64 # pixels
CHUNK = 8 # blocks
BLOCKCHUNK = BLOCK * CHUNK # pixels
BLOCKXY = Vec(BLOCK, BLOCK) # pixels
CHUNKXY = Vec(CHUNK, CHUNK) # blocks
BLOCKCHUNKXY = Vec(BLOCKCHUNK, BLOCKCHUNK) # pixels
REGION = 32 # chunks
REGIONXY = Vec(REGION, REGION) # chunks
CHUNK_CHECK_MAX_FREQ = 20 # per second
CHUNK_LOAD_MAX_FREQ = 128 # per second
AUTOSAVE_INTERVAL = 15 # seconds

class ChunkLayer(IntEnum):
    BG = auto()
    MG = auto()
    FG = auto()

__all__ = [
    "WIDTH", "HEIGHT", "SIZE", "Layer", "BLOCK", "CHUNK", "BLOCKCHUNK",
    "BLOCKXY", "CHUNKXY", "BLOCKCHUNKXY", "REGION", "REGIONXY",
    "CHUNK_CHECK_MAX_FREQ", "CHUNK_LOAD_MAX_FREQ", "AUTOSAVE_INTERVAL",
    "ChunkLayer",
]
