import json
import blueprintUtil

global gameVersion
gameVersion = 281474976710656

dataFile = "data.txt"


# Classes

class Signal(dict):
    def __init__(self, name, type="item"):
        super().__init__()

        self["name"] = name
        self["type"] = type

class Blueprint:
    "A way to create and edit blueprints. Please note that Factorio has an inverted y, this is not a bug."

    gameVersion = 281474976710656

    def __init__(self, importString=None):
        self.nextEntityNumber = 1

        if importString:
            self.data = blueprintUtil.decode(importString)

            # Update self.nextEntityNumber
            assert "blueprint" in self.data.keys()
            if "entities" in self.data["blueprint"].keys():
                for i in self.data["blueprint"]["entities"]:
                    self.nextEntityNumber = max(self.nextEntityNumber, i["entity_number"]) + 1
        else:
            self.data = {"blueprint": {
                "version": self.__class__.gameVersion, # Not really needed
                "item": "blueprint" # Not sure why some blueprints have this
            }}
    
    def getDecoded(self):
        return self.data
    
    def getEncoded(self):
        return blueprintUtil.encode(self.data)
    
    def getJSON(self):
        return json.dumps(self.data, indent=4)
    

    def setLabel(self, label):
        self.data["blueprint"]["label"] = label
    
    def setLabelColor(self, r, g, b, a=1):
        self.data["blueprint"]["label_color"] = {"r": r, "g": g, "b": b, "a": a}
    
    def setIcons(self, signals):
        assert len(signals) <= 4
        self.data["blueprint"]["icons"] = []

        for i in range(len(signals)):
            # Skip over a spot
            if not signals[i]:
                continue

            self.data["blueprint"]["icons"].append({
                "signal": signals[i],
                "index": i+1
            })
    
    def setGridSize(self, x, y):
        self.data["blueprint"]["snap-to-grid"] = makePosition(x, y)
    
    def setLockToGrid(self, value):
        self.data["blueprint"]["absolute-snapping"] = value
    

    def addEntity(self, name, x, y, rotation=0, type=False, id=None):
        "rotation is even numbers clockwise in steps of 90 deg"

        # Add entities field if not already there
        if "entities" not in self.data["blueprint"].keys():
            self.data["blueprint"]["entities"] = []

        # Set the id if not already done
        if id == None:
            id = self.nextEntityNumber
            self.nextEntityNumber += 1
        else:
            self.nextEntityNumber = max(self.nextEntityNumber, id) + 1

        # Set up the entity
        entity = {
            "entity_number": id,
            "name": name,
            "position": makePosition(x, y),
            "direction": rotation
        }

        # Add bits to the entity
        if type: entity["type"] = type

        # Add entity
        self.data["blueprint"]["entities"].append(entity)
    
    def addTile(self, name, x, y):
        # Add tiles field if not already there
        if "tiles" not in self.data["blueprint"].keys():
            self.data["blueprint"]["tiles"] = []
        
        # Add tile
        self.data["blueprint"]["tiles"].append({
            "name": name,
            "position": makePosition(x, y)
        })


# Runtime

b = Blueprint()
b.setLabel("test.py")
b.setIcons([Signal("transport-belt") for i in range(4)])

for i in range(8):
    if i % 2 == 0: # Even
        b.addEntity("underground-belt", i+0.5, -i+0.5, i, type="input")
    else:
        b.addEntity("underground-belt", i+0.5, -i+0.5, i-1, type="output")

# Printing
print(b.getJSON())
with open(dataFile, "w") as f:
    print(b.getEncoded(), file=f)