import json
import blueprintUtil

global gameVersion
gameVersion = 281474976710656

dataFile = "data.txt"


# Classes

class FixedDict(dict):
    "A dictionary that cannot have keys added or removed and starts with key-value pairs. (Intended as a parent class.)"

    start = {"key": "value"} # Overwrite when making a child class

    def __init__(self, startFilled=True):
        super().__init__()
        if startFilled:
            for k, v in self.__class__.start.items():
                self.__setitem__(k, v)

    def __setitem__(self, key, value):
        assert key in self.__class__.start.keys()
        super().__setitem__(key, value)


# Classes from https://wiki.factorio.com/Blueprint_string_format

class Color(dict):
    #start = {
    #    "r": None,
    #    "g": None,
    #    "b": None,
    #    "a": None
    #}

    def __init__(self, r, g, b, a=1):
        super().__init__()

        self["r"] = r
        self["g"] = g
        self["b"] = b
        self["a"] = a

class Signal(dict):
    #start = {
    #    "name": "prototype-name",
    #    "type": "item, fluid, or virtual"
    #}

    def __init__(self, name, type):
        super().__init__()

        self["name"] = name
        self["type"] = type

class Icon(dict):
    #start = {
    #    "index": 1,
    #    "signal": Signal("prototype-name", "item, fluid, or virtual")
    #}

    def __init__(self, signal, index):
        super().__init__()

        self["signal"] = signal
        self["index"] = index

class Position(dict):
    #start = {
    #    "x": 0,
    #    "y": 0
    #}

    def __init__(self, x, y):
        super().__init__()

        self["x"] = x
        self["y"] = y

class ConnectionPoint(dict):
    def __init__(self, entity, port=1):
        super().__init__()

        self["entity_id"] = entity
        self["circuit_id"] = port

class Connections(dict):
    def __init__(self, redFrom1=[], greenFrom1=[], redFrom2=[], greenFrom2=[]):
        "All inputs must be lists of ConnectionPoint(s)"

        # Assuring correct formatting
        redFrom1 = list(redFrom1)
        greenFrom1 = list(greenFrom1)
        redFrom2 = list(redFrom2)
        greenFrom2 = list(greenFrom2)

        super().__init__()

        self["1"] = {"red": redFrom1, "green": greenFrom1}
        self["2"] = {"red": redFrom2, "green": greenFrom2}

class Entity(dict):
    #start = {
    #    "entity_number": 1,
    #    "name": "prototype-name",
    #    "position": Position(0, 0),
    #    "direction": 0,
    #    "orientation": 0, # Trains
    #    "connections": 
    #}

    def __init__(self, number, name, position, **kwargs):#, startFilled=False):
        super().__init__()#startFilled)

        self["entity_number"] = number
        self["name"] = name
        self["position"] = position

        for k, v in kwargs.items():
            self[k] = v

class Blueprint(dict):
    #start = {
    #    "item": "blueprint",
    #    "label": "Blueprint made using Python",
    #    "label_color": Color(0, 0, 0, 0),
    #    "entities": [],
    #    "tiles": [],
    #    "icons": [],
    #    "schedules": [],
    #    "version": gameVersion
    #}

    def __init__(self, entities=[], **kwargs):
        super().__init__()

        self["item"] = "blueprint"
        self["version"] = gameVersion
        self["entities"] = entities

        for k, v in kwargs.items():
            self[k] = v
    
    def getDecoded(self):
        return {"blueprint": self}
    
    def getEncoded(self):
        return blueprintUtil.encode(self.getDecoded())
    
    def getJSON(self):
        return json.dumps(self.getDecoded(), indent=4)

class BlueprintBook(dict):
    #start = {
    #    "item": "blueprint-book",
    #    "label": "Blueprint book made using Python",
    #    "label_color": Color(0, 0, 0, 0),
    #    "blueprints": {},
    #    "active_index": 0,
    #    "version": gameVersion
    #}

    def __init__(self, blueprints, **kwargs):
        super().__init__()

        self["item"] = "blueprint-book"
        self["version"] = gameVersion
        self["blueprints"] = blueprints

        for k, v in kwargs.items():
            self[k] = v
    
    def getDecoded(self):
        return {"blueprint_book": self}
    
    def getEncoded(self):
        return blueprintUtil.encode(self.getDecoded())
    
    def getJSON(self):
        return json.dumps(self.getDecoded(), indent=4)


# Runtime

b = Blueprint({
    "label": "Blueprint made using Python",
    "entities": [
        Entity(1, "transport-belt", Position(0, 0), connections=Connections([
            ConnectionPoint(2)
        ])),
        Entity(2, "transport-belt", Position(1, 0), connections=Connections([
            ConnectionPoint(1)
        ]))
    ]
})

#b = Blueprint()
#b.setLabel("test.py")
#b.setIcons([makeSignal("transport-belt") for i in range(4)])

#for i in range(8):
#    if i % 2 == 0: # Even
#        b.addEntity("underground-belt", i+0.5, -i+0.5, i, type="input")
#    else:
#        b.addEntity("underground-belt", i+0.5, -i+0.5, i-1, type="output")

# Printing
print(b.getJSON())
with open(dataFile, "w") as f:
    print(b.getEncoded(), file=f)
