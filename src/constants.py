from src.utils import Vec as _Vec

WIDTH, HEIGHT = 1280, 768 # pixels
SIZE = _Vec(WIDTH, HEIGHT) # pixels

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
