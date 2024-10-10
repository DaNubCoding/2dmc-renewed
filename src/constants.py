from src.utils import Vec

WIDTH, HEIGHT = 1280, 768 # pixels
SIZE = Vec(WIDTH, HEIGHT) # pixels

BLOCK = 64 # pixels
CHUNK = 8 # blocks
BLOCKCHUNK = BLOCK * CHUNK # pixels
BLOCKXY = Vec(BLOCK, BLOCK) # pixels
CHUNKXY = Vec(CHUNK, CHUNK) # blocks
BLOCKCHUNKXY = Vec(BLOCKCHUNK, BLOCKCHUNK) # pixels
REGION = 32 # chunks
REGIONXY = Vec(REGION, REGION) # chunks
CHUNK_CHECK_MAX_FREQ = 20 # per second
CHUNK_LOAD_MAX_FREQ = 1024 # per second
AUTOSAVE_INTERVAL = 15 # seconds
