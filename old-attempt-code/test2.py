import json
import blueprintUtil

global gameVersion
gameVersion = 281474976710656

dataFile = "data.txt"


# Classes

class Signal(dict):
    #start = {
    #    "name": "prototype-name",
    #    "type": "item, fluid, or virtual"
    #}

    def __init__(self, name, type):
        super().__init__()

        self["name"] = name
        self["type"] = type

class Blueprint:
    "A way to create and edit blueprints. Please note that Factorio has an inverted y, this is not a bug. Be careful when editing data directly; it is easy to corrupt it, so you might want to use the shortcuts provided."
    
    def __init__(self):
        "Sets up variables"

        self.nextEntityNumber = 1
        self.nextTileNumber = 1
        #self.

        self.data = {
            "blueprint": {
                "item": "blueprint",
                "label": "",
                "label_color": {},
                "entities": [],
                "tiles": [],
                "icons": [],
                "schedules": [],
                "version": gameVersion,
            }
        }

        # Shortcuts
        self.main = self.data["blueprint"]


    def importDecoded(self, data, overwrite=True):
        if overwrite:
            self.data.update(data)
        else:
            # It is not done in a single line, to avoid deleting self.data
            data = data.copy()
            data.update(self.data)
            self.data = data
    
    def importEncoded(self, string):
        self.importDecoded(blueprintUtil.decode(string))

    def importJSON(self, string):
        self.importDecoded(json.loads(string))

    
    def getDecoded(self):
        return self.data
    
    def getEncoded(self):
        return blueprintUtil.encode(self.data)
    
    def getJSON(self):
        return json.dumps(self.data, indent=4)
    

    def setLabel(self, label):
        self.main["label"] = label
    
    def setLabelColor(self, r, g, b, a=1):
        self.main["blueprint"]["label_color"] = {"r": r, "g": g, "b": b, "a": a}


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