import json
import encode_decode

class BlueprintIcon:
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

class Blueprint:
    VERSION = 281479277379584

    def __init__(self) -> None:
        self.entities = []

        self.icons = [BlueprintIcon()]

    def to_dict(self):
        entities = []
        for index, entity in enumerate(self.entities):
            e = {"entity_number": index+1}
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

class ConstantCombinator(Entity):
    def __init__(self, x, y) -> None:
        super().__init__("constant-combinator", x, y)

blueprint = Blueprint()
blueprint.entities.append(Entity("wooden-chest", 0.5, 0.5))
blueprint.entities.append(ConstantCombinator(2.5, 0.5))

print(blueprint.to_json())
print(blueprint.to_encoded())

