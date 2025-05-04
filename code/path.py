import os

BASE_DIR = os.path.dirname(__file__)
ASSET = lambda *parts: os.path.join(BASE_DIR, "..", *parts)