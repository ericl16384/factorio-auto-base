import json
import combinator_operations as co

import encode_decode


class Blueprint:
    VERSION = 281479277379584
    MAX_WIRE_LENGTH = 10
    

    class Connection:
        def __init__(self, color, entity_1, entity_2, port_1, port_2) -> None:
            self.color = color
            self.entity_1 = entity_1
            self.entity_2 = entity_2
            self.port_1 = port_1
            self.port_2 = port_2

            # self.connections = [
            #     (self.entity_1, self.port_1), (self.entity_2, self.port_1)
            # ]
        
        def add_self_to_connection_lookup(self, lookup):
            # 1 and 2 are identical inverses


            if self.entity_1 not in lookup:
                lookup[self.entity_1] = {}

            if self.port_1 not in lookup[self.entity_1]:
                lookup[self.entity_1][self.port_1] = {}

            if self.color not in lookup[self.entity_1][self.port_1]:
                lookup[self.entity_1][self.port_1][self.color] = []

            lookup[self.entity_1][self.port_1][self.color].append(
                {"entity_id": self.entity_2}
            )


            if self.entity_2 not in lookup:
                lookup[self.entity_2] = {}

            if self.port_2 not in lookup[self.entity_2]:
                lookup[self.entity_2][self.port_2] = {}

            if self.color not in lookup[self.entity_2][self.port_2]:
                lookup[self.entity_2][self.port_2][self.color] = []

            lookup[self.entity_2][self.port_2][self.color].append(
                {"entity_id": self.entity_1}
            )


    def __init__(self) -> None:
        self.entities = []
        self.connections = []

        self.icons = [IconSignal("wooden-chest", "item")]
    
    def add_entity(self, entity):
        self.entities.append(entity)
        return len(self.entities)
    
    def add_connection(self, color, entity_1, entity_2, port_1=1, port_2=1):
        connection = self.Connection(
            color, entity_1, entity_2, port_1, port_2
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
        for index, entity in enumerate(self.entities):
            e = {}

            if isinstance(entity, LogicCombinator):
                e["control_behavior"] = entity.conditions.to_dict()

            if index + 1 in connection_lookup:
                e["connections"] = connection_lookup[index + 1]

            e["entity_number"] = index + 1
            e.update(entity.to_dict())
            entities.append(e)
        
        icons = []
        for index, icon in enumerate(self.icons):
            i = {"index": index + 1}
            i.update(icon.to_dict())
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
    def __init__(self, name, x, y) -> None:
        self.name = name
        self.x = x
        self.y = y
    
    def to_dict(self):
        return {"name": self.name, "position": {
            "x": self.x, "y": self.y
        }}

class Signal:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type
        
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type
        }

class IconSignal(Signal):
    def to_dict(self):
        return {
            "signal": super().to_dict()
        }
    
class CombinatorConditions:
    def __init__(self, input, output, operation, second=0) -> None:
        self.operation = operation

        self.copy_count_from_input = True

        self.signal_1 = input
        self.output_signal = output

        self.signal_2 = None
        self.constant = 0
        if isinstance(second, Signal):
            self.signal_2 = second
        else:
            assert isinstance(second, int)
            self.constant = second
    
    def to_dict(self):
        if self.operation in co.arithmetic:
            return {"arithmetic_conditions": self.get_arithmetic_dict()}
        elif self.operation in co.decider:
            return {"decider_conditions": self.get_decider_dict()}
        else:
            assert False, self.operation

    def get_arithmetic_dict(self):
        d = {}

        # d["copy_count_from_input"] = self.copy_count_from_input

        d["first_signal"] = self.signal_1.to_dict()
        
        d["operation"] = self.operation

        d["output_signal"] = self.output_signal.to_dict()

        if self.signal_2:
            d["second_signal"] = self.signal_2.to_dict()
        else:
            d["second_constant"] = self.constant
        
        return d

    def get_decider_dict(self):
        d = {}
        
        d["comparator"] = self.operation

        if not self.signal_2:
            d["constant"] = self.constant

        d["copy_count_from_input"] = self.copy_count_from_input

        d["first_signal"] = self.signal_1.to_dict()

        d["output_signal"] = self.output_signal.to_dict()

        if self.signal_2:
            d["second_signal"] = self.signal_2.to_dict()
        
        return d


class WoodenChest(Entity):
    def __init__(self, x, y) -> None:
        super().__init__("wooden-chest", x, y)

class ConstantCombinator(Entity):
    def __init__(self, x, y) -> None:
        super().__init__("constant-combinator", x, y)

class LogicCombinator(Entity):
    pass

class DeciderCombinator(LogicCombinator):
    def __init__(self, x, y, conditions: CombinatorConditions) -> None:
        super().__init__("decider-combinator", x, y)
        self.conditions = conditions

class ArithmeticCombinator(LogicCombinator):
    def __init__(self, x, y, conditions: CombinatorConditions) -> None:
        super().__init__("arithmetic-combinator", x, y)
        self.conditions = conditions




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

    c = CombinatorConditions(
        Signal("inserter", "item"),
        Signal("long-handed-inserter", "item"),
        co.LESS_THAN
    )
    dc = blueprint.add_entity(DeciderCombinator(0.5, 0, c))

    c = CombinatorConditions(
        Signal("inserter", "item"),
        Signal("long-handed-inserter", "item"),
        co.GREATER_THAN,
        Signal("signal-3", "virtual")
    )
    dc = blueprint.add_entity(DeciderCombinator(1.5, 0, c))

    c = CombinatorConditions(
        Signal("inserter", "item"),
        Signal("long-handed-inserter", "item"),
        co.MULTIPLY
    )
    dc = blueprint.add_entity(ArithmeticCombinator(2.5, 0, c))

    c = CombinatorConditions(
        Signal("inserter", "item"),
        Signal("long-handed-inserter", "item"),
        co.MULTIPLY,
        Signal("signal-4", "virtual")
    )
    dc = blueprint.add_entity(ArithmeticCombinator(3.5, 0, c))
    


    print(blueprint.to_json())
    print(blueprint.to_encoded())

    with open("custom_blueprint.json", "w") as f:
        print(blueprint.to_json(), file=f)

