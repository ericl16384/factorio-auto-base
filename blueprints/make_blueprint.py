import json
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

        self.icons = [Icon()]
    
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
            if index+1 in connection_lookup:
                e["connections"] = connection_lookup[index+1]
            e["entity_number"] = index+1
            e.update(entity.to_dict())
            entities.append(e)
        
        icons = []
        for index, icon in enumerate(self.icons):
            i = {"index": index+1}
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

class Icon:
    def __init__(self) -> None:
        self.name = "wooden-chest"
        self.type = "item"
    
    def to_dict(self):
        return {
            "signal": {
                "name": self.name,
                "type": self.type
            }
        }


class WoodenChest(Entity):
    def __init__(self, x, y) -> None:
        super().__init__("wooden-chest", x, y)

class ConstantCombinator(Entity):
    def __init__(self, x, y) -> None:
        super().__init__("constant-combinator", x, y)


blueprint = Blueprint()


previous_id1 = None
previous_id2 = None

for i in range(20):
    id1 = blueprint.add_entity(WoodenChest(0.5, 0.5+i))
    id2 = blueprint.add_entity(ConstantCombinator(1.5+i, 0.5+i))

    blueprint.add_connection("red", id1, id2)

    if previous_id1:
        blueprint.add_connection("green", id1, previous_id1)
    if previous_id2:
        blueprint.add_connection("green", id2, previous_id2)

    previous_id1 = id1
    previous_id2 = id2


print(blueprint.to_json())
print(blueprint.to_encoded())

with open("blueprints/custom_blueprint.json", "w") as f:
    print(blueprint.to_json(), file=f)

