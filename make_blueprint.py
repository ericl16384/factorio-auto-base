import json
import combinator_operations as co

import encode_decode


class Blueprint:
    VERSION = 281479277379584
    MAX_WIRE_LENGTH = 10 # not yet used, but factorio enforced
    

    class Connection:
        def __init__(self, color, entityA, entityB, portA, portB) -> None:
            self.color = color
            self.entityA = entityA
            self.entityB = entityB
            self.portA = portA
            self.portB = portB

            # self.connections = [
            #     (self.entityA, self.portA), (self.entityB, self.portA)
            # ]
        
        def prepare_entity_in_connection_lookup(self, lookup, entity, port):
            if entity not in lookup:
                lookup[entity] = {}

            if port not in lookup[entity]:
                lookup[entity][port] = {}

            if self.color not in lookup[entity][port]:
                lookup[entity][port][self.color] = []
        
        def add_self_to_connection_lookup(self, lookup):
            self.prepare_entity_in_connection_lookup(lookup, self.entityA, self.portA)

            lookup[self.entityA][self.portA][self.color].append({
                "circuit_id": self.portB,
                "entity_id": self.entityB
            })


            self.prepare_entity_in_connection_lookup(lookup, self.entityB, self.portB)

            lookup[self.entityB][self.portB][self.color].append({
                "circuit_id": self.portA,
                "entity_id": self.entityA
            })


    def __init__(self) -> None:
        self.entities = {}

        self.circuits = {}
        self.connections = []

        self.next_entity_number = 1

        self.icons = [IconSignal("wooden-chest", "item")]
    
    def add_entity(self, entity):
        i = self.next_entity_number
        self.next_entity_number += 1

        self.entities[i] = entity
        return i
    
    def add_connection(self, color, entityA, entityB, portA, portB):
        connection = self.Connection(
            color, entityA, entityB, portA, portB
        )
        self.connections.append(connection)
    
    def get_connection_lookup(self):
        lookup = {}
        for c in self.connections:
            c.add_self_to_connection_lookup(lookup)
        return lookup

    def to_dict(self):
        connection_lookup = self.get_connection_lookup()

        entities = []
        for entity_number in self.entities:
            entity = self.entities[entity_number]
            e = {}

            if entity.control_behavior != None:
                e["control_behavior"] = entity.control_behavior.to_dict()

            if entity_number in connection_lookup:
                e["connections"] = connection_lookup[entity_number]

            e["entity_number"] = entity_number
            e.update(entity.to_dict())
            entities.append(e)
        
        icons = []
        for index, icon in enumerate(self.icons):
            i = {"index": index + 1}
            i.update(icon)
            icons.append(i)

        return {"blueprint": {
            "entities": entities,
            "icons": icons,
            "item": "blueprint",
            "version": self.VERSION
        }}

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
    
    def to_encoded(self):
        return encode_decode.encode(self.to_json(0))

class Entity:
    def __init__(self, name, x, y, control_behavior=None) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.control_behavior = control_behavior
    
    def to_dict(self):
        return {"name": self.name, "position": {
            "x": self.x, "y": self.y
        }}
    
class Signal(dict):
    def __init__(self, name, type) -> None:
        super().__init__()
        self["name"] = name
        self["type"] = type

        # self.name = name
        # self.type = type
        
    # def to_dict(self):
    #     return {
    #         "name": self.name,
    #         "type": self.type
    #     }

    def __hash__(self):
        return hash(self["name"]) + hash(self["type"])

class IconSignal(dict):
    def __init__(self, name, type) -> None:
        super().__init__()
        self["signal"] = Signal(name, type)

    # def to_dict(self):
    #     return {
    #         "signal": super().to_dict()
    #     }

class ControlBehavior:#(dict):
    pass

class ConstantCombinatorConditions(ControlBehavior):
    def __init__(self, signal_count_pairs: list) -> None:
        super().__init__()

        assert len(signal_count_pairs) <= 20
        self.signal_count_pairs = signal_count_pairs
    
    def to_dict(self):
        d = {"filters": []}
        for i, signal_count in enumerate(self.signal_count_pairs):
            signal, count = signal_count
            assert isinstance(signal, dict), signal
            d["filters"].append({
                "count": count,
                "index": i + 1,
                "signal": signal
            })
        return d
    
class LogicCombinatorConditions(ControlBehavior):
    def __init__(self, input, output, operation, second=0, copy_count=False) -> None:
        super().__init__()

        self.operation = operation

        self.copy_count_from_input = copy_count

        self.signal_1 = input
        self.output_signal = output

        self.signal_2 = None
        self.constant = 0
        if isinstance(second, Signal):
            self.signal_2 = second
        elif isinstance(second, int):
            self.constant = second
        else:
            assert False, second
    
    def to_dict(self):
        if self.operation in co.arithmetic:
            return {"arithmetic_conditions": self.get_arithmetic_dict()}
        elif self.operation in co.decider:
            return {"decider_conditions": self.get_decider_dict()}
        else:
            assert False, self.operation

    def get_arithmetic_dict(self):
        d = {}

        assert not self.copy_count_from_input
        # d["copy_count_from_input"] = self.copy_count_from_input

        d["first_signal"] = self.signal_1
        
        d["operation"] = self.operation

        d["output_signal"] = self.output_signal

        if self.signal_2:
            d["second_signal"] = self.signal_2
        else:
            d["second_constant"] = self.constant
        
        return d

    def get_decider_dict(self):
        d = {}
        
        d["comparator"] = self.operation

        if not self.signal_2:
            d["constant"] = self.constant

        d["copy_count_from_input"] = self.copy_count_from_input

        d["first_signal"] = self.signal_1

        d["output_signal"] = self.output_signal

        if self.signal_2:
            d["second_signal"] = self.signal_2
        
        return d
    
class CircuitCondition(ControlBehavior):
    def __init__(self, first, comparator, second) -> None:
        super().__init__()

        self.first = first
        self.second = second

        self.comparator = comparator
        self.second = 0
        if isinstance(second, Signal):
            self.second = second
        elif isinstance(second, int):
            self.constant = second
        else:
            assert False, second
    
    def to_dict(self):
        d = {}

        d["comparator"] = self.comparator
        if not self.second:
            d["constant"] = self.constant
        d["first_signal"] = self.first

        assert not self.second
        # d["second_signal"] = self.second

        return {"circuit_condition": d}

class LampCondition(CircuitCondition):
    def __init__(self, first, comparator, second, use_color=False) -> None:
        super().__init__(first, comparator, second)
        self.use_color = use_color
    
    def to_dict(self):
        d = super().to_dict()
        if self.use_color:
            d["use_color"] = self.use_color
        return d

class WoodenChest(Entity):
    def __init__(self, x, y) -> None:
        super().__init__("wooden-chest", x, y)

class SmallElectricPole(Entity):
    def __init__(self, x, y) -> None:
        super().__init__("small-electric-pole", x, y)

class Substation(Entity):
    def __init__(self, x, y) -> None:
        super().__init__("substation", x, y)

class ConstantCombinator(Entity):
    def __init__(self, x, y, control_behavior: ConstantCombinatorConditions) -> None:
        super().__init__("constant-combinator", x, y, control_behavior)

class DeciderCombinator(Entity):
    def __init__(self, x, y, control_behavior: LogicCombinatorConditions) -> None:
        super().__init__("decider-combinator", x, y, control_behavior)

class ArithmeticCombinator(Entity):
    def __init__(self, x, y, control_behavior: LogicCombinatorConditions) -> None:
        super().__init__("arithmetic-combinator", x, y, control_behavior)

class Lamp(Entity):
    def __init__(self, x, y, control_behavior: CircuitCondition) -> None:
        super().__init__("small-lamp", x, y, control_behavior)



if __name__ == "__main__":
    blueprint = Blueprint()


    # previous_id1 = None
    # previous_id2 = None

    # for i in range(20):
    #     id1 = blueprint.add_entity(WoodenChest(0.5, 0.5+i))
    #     id2 = blueprint.add_entity(ConstantCombinator(1.5+i, 0.5+i))

    #     blueprint.add_connection("red", id1, id2)

    #     if previous_id1:
    #         blueprint.add_connection("green", id1, previous_id1)
    #     if previous_id2:
    #         blueprint.add_connection("green", id2, previous_id2)

    #     previous_id1 = id1
    #     previous_id2 = id2

    c = LogicCombinatorConditions(
        Signal("inserter", "item"),
        Signal("long-handed-inserter", "item"),
        co.LESS_THAN
    )
    dc1 = blueprint.add_entity(DeciderCombinator(0.5, 0, c))

    c = LogicCombinatorConditions(
        Signal("inserter", "item"),
        Signal("long-handed-inserter", "item"),
        co.GREATER_THAN,
        Signal("signal-3", "virtual")
    )
    dc2 = blueprint.add_entity(DeciderCombinator(1.5, 0, c))

    c = LogicCombinatorConditions(
        Signal("inserter", "item"),
        Signal("long-handed-inserter", "item"),
        co.MULTIPLY
    )
    ac1 = blueprint.add_entity(ArithmeticCombinator(2.5, 0, c))

    c = LogicCombinatorConditions(
        Signal("inserter", "item"),
        Signal("long-handed-inserter", "item"),
        co.MULTIPLY,
        Signal("signal-4", "virtual")
    )
    ac2 = blueprint.add_entity(ArithmeticCombinator(3.5, 0, c))

    blueprint.add_connection("red", dc1, dc2, 1, 1)
    blueprint.add_connection("red", dc1, dc2, 2, 2)
    blueprint.add_connection("green", ac1, ac2, 2, 2)
    blueprint.add_connection("green", ac1, ac2, 1, 1)

    c1 = blueprint.add_entity(ConstantCombinator(4.5, 0, ConstantCombinatorConditions([
        (Signal("signal-5", "virtual"), 42),
        (Signal("signal-H", "virtual"), 12)
    ])))
    


    # print(blueprint.to_json())
    print(blueprint.to_encoded())

    with open("custom_blueprint.json", "w") as f:
        print(blueprint.to_json(), file=f)

