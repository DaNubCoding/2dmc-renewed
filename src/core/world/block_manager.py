from bidict import bidict
import json

class BlockManager:
    def __init__(self) -> None:
        with open("res/data/blocks/names.json") as file:
            # Mapping of block names to block ids
            self.ids = bidict({
                name: id for id, name in enumerate(json.load(file))
            })
            # Mapping of block ids to block names
            self.names = self.ids.inverse
