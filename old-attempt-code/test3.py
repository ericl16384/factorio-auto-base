"A utility for making Factorio blueprints. It is recommended to not edit your blueprint, only add to it, as it is easy to corrupt the data. Alternatively, you can use the built-in methods."

import json, math
import blueprintUtil


# Classes


class Proto:
    def __init__(self, type, **kwargs):
        "A way of creating multiple similar objects with slight changes. Please refer to the respective objects' inputs. Then, use the create() method to make an instance."

        super().__init__()

        self.type = type
        self.data = kwargs

    def __repr__(self):
        return f"Proto({self.type}, **kwargs={self.data})"
    
    def __str__(self):
        return self.__repr__()
    
    def create(self, **kwargs):
        "Use the kwargs to override your default perameters."

        data = self.data.copy()
        data.update(kwargs)
        return self.type(data)


class Signal(dict):
    def __init__(self, prototypeName, signalType=0):
        "signal types: item (0), fluid (1), virtual (2)"

        super().__init__()

        if signalType == 0:
            signalType = "item"
        elif signalType == 1:
            signalType = "fluid"
        elif signalType == 2:
            signalType = "virtual"

        self["type"] = signalType
        self["name"] = prototypeName

class Connections(dict):
    def __init__(self, red1=[], green1=[], red2=[], green2=[]):
        """exampleFormat = [
            {"entity_id": 42, "circuit_id": 1}, # Connecting to the input of combinator 42
            {"entity_id": 64, "circuit_id": 2}, # Connecting to the output of combinator 64
            {"entity_id": 128}, # Connecting to entity 128 something else
        ]
        # Also, a one-way connection works as a two-way connection, and a missing circuit_id is assumed to be set to 1."""

        super().__init__()

        if red1 or green1:
            self["1"] = {}
            if red1:
                self["1"]["red"] = red1
            if green1:
                self["1"]["green"] = green1

        if red2 or green2:
            self["2"] = {}
            if red1:
                self["2"]["red"] = red2
            if green1:
                self["2"]["green"] = green2

class Entity(dict):
    def __init__(self, number, name, x, y, invertY=True, offsetPosition=False, **kwargs):
        """invertY makes y be up, not down.
        offsetPosition adds 0.5 to x and y, so that the entity is in the middle of the tile, rather than on the bottom left corner."""

        super().__init__()

        self["entity_number"] = number
        self["name"] = name
        self["position"] = {"x": x, "y": y}
        # direction
        # connections

        if invertY:
            self["position"]["y"] *= -1
        if offsetPosition:
            self["position"]["x"] += 0.5
            self["position"]["y"] += 0.5
        
        # kwargs
        while "kwargs" in kwargs.keys():
            kwargs = kwargs["kwargs"]
        self.update(kwargs)

class ConstantCombinator(Entity):
    def __init__(self, number, x, y, constants=[], **kwargs):
        "constant-combinator"
        
        super().__init__(number, "constant-combinator", x, y, kwargs=kwargs)

        self["control_behavior"] = {}
        self["control_behavior"]["filters"] = constants
        
        ## kwargs
        #self.update(kwargs)

class Combinator(Entity):
    # Modes
    arithmetic = ["+", "-", "*", "/", "%", "^", "<<", ">>", "AND", "OR", "XOR"]
    decider = ["<", ">", "=", "≤", "≥", "≠"]

    def __init__(self, number, x, y, mode, firstSignal=None, secondSignal=None, outputSignal=None, firstConstant=None, secondConstant=None, **kwargs):
        "arithmetic-combinator or decider-combinator"

        # Setup data and super().__init__()
        
        # arithmetic-combinator
        if mode in self.__class__.arithmetic:
            super().__init__(number, "arithmetic-combinator", x, y, kwargs=kwargs)

            self["control_behavior"] = {}
            self["control_behavior"]["arithmetic_conditions"] = {}

            data = self["control_behavior"]["arithmetic_conditions"]

        # decider-combinator
        elif mode in self.__class__.decider:
            super().__init__(number, "decider-combinator", x, y, kwargs=kwargs)

            self["control_behavior"] = {}
            self["control_behavior"]["decider_conditions"] = {}

            data = self["control_behavior"]["decider_conditions"]

        # unknown!!!
        else:
            raise ValueError(f"mode must be in {self.__class__.__name__}.arithmetic or {self.__class__.__name__}.decider")


        # Fill data

        data["operation"] = mode

        if firstSignal:
            data["first_signal"] = firstSignal
        if secondSignal:
            data["second_signal"] = secondSignal
        if outputSignal:
            data["output_signal"] = outputSignal
        
        if firstConstant or firstConstant == 0:
            data["first_constant"] = firstConstant
        if secondConstant or secondConstant == 0:
            data["second_constant"] = secondConstant
        

        ## kwargs
        #
        #self.update(kwargs)

class Controllable(Entity):
    def __init__(self, number, name, x, y, mode, firstSignal=None, secondSignal=None, constant=None, **kwargs):
        assert mode in Combinator.decider

        super().__init__(number, name, x, y, kwargs=kwargs)

        self["control_behavior"] = {}
        self["control_behavior"]["circuit_condition"] = {}
        data = self["control_behavior"]["circuit_condition"]

        if firstSignal:
            data["first_signal"] = firstSignal
        if secondSignal:
            data["second_signal"] = secondSignal
        if constant or constant == 0:
            data["constant"] = constant
        
        ## kwargs
        #self.update(kwargs)


class CircuitNetwork:
    def __init__(self, channels=[]):
        self.channels = channels
    def __call__(self): # Shorthand for new()
        return self.new()
    def __add__(self, other): # Combining networks
        channels = self.channels.copy()
        channels.extend(other.channels)

        x = self.__class__(channels)
        x.cleanup()
        return x


    def new(self, channel=None):
        if not channel:
            channel = self.Channel()
        else:
            assert channel not in self.channels

        self.channels.append(channel)
        return channel
        
    def cleanup(self):
        # Remove duplicate channels

        i = 0
        while i < len(self.channels):

            j = i + 1
            while j < len(self.channels):
                # Channel objects handle "==" differently, so use hash()
                if hash(self.channels[i]) == hash(self.channels[j]):
                    # If identical, remove the second one
                    self.channels.pop(j)

                else:
                    # Move on to the next comparison
                    j += 1
            
            # Cleanup the current channel
            self.channels[i].cleanup()

            i += 1
        

        # Anything more???

    def export(self):
        self.cleanup()
        return self.channels


    class Channel: # https://docs.python.org/3/reference/datamodel.html#special-method-names
        def __init__(self):
            self.data = []
        def __call__(self, x):
            self.data.append(x)
        def __hash__(self):
            # Dicts are not hashable, so convert the dicts to tuples of key value pairs
            return hash([i.items() for i in self.data])
        
        def add(self, x):
            self.__call__(x)
        
        def cleanup(self):
            # Add duplicate combinators

            i = 0
            while i < len(self.channels):

                j = i + 1
                while j < len(self.channels):
                    if self.data[i] == self.data[j]:
                        # If identical, add them, and remove the second one
                        second = self.channels.pop(j)

                    else:
                        # Move on to the next comparison
                        j += 1
                
                # Cleanup the current channel
                self.channels[i].cleanup()

                i += 1
            

            # Anything more???

        # Arithmetic
        def __add__(self, other):
            return [self, "+", other]
        def __sub__(self, other):
            return [self, "-", other]
        def __mul__(self, other):
            return [self, "*", other]
        #def __matmul__(self, other): # Matrix multiplication
        #    return
        #def __div__(self, other): # No! Use __truediv__()
        #    return
        def __truediv__(self, other): # Shorthand for __floordiv__()
            return self.__floordiv__(other)
        def __floordiv__(self, other):
            return [self, "/", other]
        def __mod__(self, other):
            return [self, "%", other]
        #def __divmod__(self, other): # I will make use of divmod() later, but there is no combinator for it...
        #    return
        def __pow__(self, other):
            return [self, "^", other]
        def __lshift__(self, other):
            return [self, "<<", other]
        def __rshift__(self, other):
            return [self, ">>", other]
        def __and__(self, other):
            return [self, "AND", other]
        def __or__(self, other):
            return [self, "OR", other]
        def __xor__(self, other):
            return [self, "XOR", other]


        # Decider
        def __lt__(self, other):
            return [self, "<", other]
        def __le__(self, other):
            return [self, "≤", other]
        def __eq__(self, other):
            return [self, "=", other]
        def __ne__(self, other):
            return [self, "≠", other]
        def __gt__(self, other):
            return [self, ">", other]
        def __ge__(self, other):
            return [self, "≥", other]

class Blueprint(dict):
    def __init__(self, data={"blueprint": {}}):
        super().__init__()
        self.update(data)


    def getDecoded(self):
        return self.copy()
    
    def getEncoded(self):
        return blueprintUtil.encode(self.getDecoded())
    
    def getJSON(self):
        return json.dumps(self.getDecoded(), indent=4)


    def addEntities(self, entities):
        if "entities" not in self["blueprint"].keys():
            self["blueprint"]["entities"] = []
        self["blueprint"]["entities"].extend(entities)

    def addCombinators(self, circuitNetwork, bounds=None):
        """Example of a flashing light:
            network = CircuitNetwork()

            time = network.add()
            time(time+1)

            mod = network.add()
            mod(time%120)

            out = network.add()
            out(mod<60)

            blueprint = Blueprint()
            blueprint.addEntities([Controllable(1, "small-lamp", 0, 0, ">", out, constant=0)])
            blueprint.addCircuitNetwork(network, [[0, 1], [1, 3]])
        """


        # Init

        circuitNetwork = circuitNetwork.export()
        entities = []
        if len(self["blueprint"]["entities"]) > 0:
            entityNumberStart = max([i["entity_number"] for i in self["blueprint"]["entities"]]) + 1
        else:
            entityNumberStart = 1
        

        # Make entities

        pass


        # Apply entities

        self.addEntities(entities)


# Constants

from string import ascii_lowercase as alphabet

signals = []
for i in range(10):
    signals.append(Signal("signal-"+str(i), 2))
for i in alphabet:
    signals.append(Signal("signal-"+i.upper(), 2))
for i in ["red", "green", "blue", "yellow", "pink", "cyan", "white", "grey", "black", "check", "info", "dot"]:
    signals.append(Signal("signal-"+i, 2))

wildcards = ["signal-everything", "signal-anything", "signal-each"]

signalRange = range(-2**31, 2**31) # Signed 32-bit number WILL OVERFLOW/UNDERFLOW


# Blueprint construction

b = Blueprint({"blueprint": {
    "icons": [
        {"signal": Signal("arithmetic-combinator"), "index": 1},
        {"signal": Signal("decider-combinator"), "index": 2},
        {"signal": Signal("red-wire"), "index": 3},
        {"signal": Signal("green-wire"), "index": 4}
    ],
    "entities": [
        #{
        #    "entity_number": 1,
        #    "name": "arithmetic-combinator",
        #    "position": {"x": 0, "y": 0},
        #    "control_behavior": {
        #        "arithmetic_conditions": {
        #            #"first_constant": 1,
        #            #"second_constant": 1,
        #            "first_signal": Signal("signal-A", 2),
        #            "second_signal": Signal("signal-B", 2),
        #            "operation": "+",
        #            "output_signal": Signal("signal-C", 2)
        #        }
        #    }
        #}

        #Combinator(1, 0, 0, "<"),#, connections=Connections([{"entity_id": 2}])),
        #ConstantCombinator(2, 0, -1, [
        #    {"signal": signals[i], "index": i+1, "count": i+1} for i in range(18) # NOT 20!!!
        #], connections=Connections([{"entity_id": 1}]))#, "circuit_id": 1}]))
    ]
}})

network = CircuitNetwork()

time = network.add()
time(time+1)

mod = network.add()
mod(time%120)

out = network.add()
out(mod<60)

blueprint = Blueprint()
blueprint.addEntities([Controllable(1, "small-lamp", 0, 0, ">", out, constant=0)])
blueprint.addCircuitNetwork(network, [[0, 1], [1, 3]])

#b.addCombinatorCode("""
#    time = time + 1
#    mod = time % 120
#    out = mod < 60
#""")

#b.addCombinatorCode([
#    Proto(Combinator, mode="+", secondConstant=1),
#    Proto(Combinator, mode="%", secondConstant=120),
#    Proto(Combinator, mode="<", secondConstant=60)
#], [
#    {
#        "from": [0],
#        "to": [0, 1]
#    },
#    {
#        "from": [1],
#        "to": [2]
#    },
#    {
#        "from": [-1],
#        "xy": [[0, -1]]
#    }
#])


# Printing

#print(json.dumps(b, indent=4))
print(b.getJSON())
with open("data.txt", "w") as f:
    print(b.getEncoded(), file=f)
