from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # points to pirate-cove/

def ASSET(*path_parts):
    return str(BASE_DIR.joinpath(*path_parts))