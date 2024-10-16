from src.util import Vec as _Vec
from enum import IntEnum as _IntEnum, auto as _auto, Enum as _Enum

WIDTH, HEIGHT = 1280, 768 # pixels
SIZE = _Vec(WIDTH, HEIGHT) # pixels

class Layer(_Enum):
    BG = _auto()
    MG = _auto()
    PLAYER = _auto()
    FG = _auto()
    HUD = _auto()
    CROSSHAIR = _auto()

BLOCK = 64 # pixels
CHUNK = 8 # blocks
BLOCKCHUNK = BLOCK * CHUNK # pixels
BLOCKXY = _Vec(BLOCK, BLOCK) # pixels
CHUNKXY = _Vec(CHUNK, CHUNK) # blocks
BLOCKCHUNKXY = _Vec(BLOCKCHUNK, BLOCKCHUNK) # pixels
REGION = 32 # chunks
REGIONXY = _Vec(REGION, REGION) # chunks
CHUNK_CHECK_MAX_FREQ = 20 # per second
CHUNK_LOAD_MAX_FREQ = 128 # per second
AUTOSAVE_INTERVAL = 15 # seconds

class ChunkLayer(_IntEnum):
    BG = _auto()
    MG = _auto()
    FG = _auto()
