class Assets:
    def __init__(self, manual: str = None, cad: str = None, image: str = None):
        self.manual = manual
        self.cad = cad
        self.image = image


class Materials:
    def __init__(self, part_number: str = None, description: str = None, quantity: int = None):
        self.part_number = part_number
        self.description = description
        self.quantity = quantity


class Specs:
    def __init__(self, hp: str = None, voltage: str = None, rpm: str = None, frame: str = None):
        self.hp = hp
        self.voltage = voltage
        self.rpm = rpm
        self.frame = frame


class Product:
    def __init__(self, product_id: str, product_category: str):
        self.product_id = product_id
        self.category = product_category
        self.description = None
        self.specs = Specs()
        self.bom = []
        self.assets = Assets()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "category": self.category,
            "description": self.description,
            "specs": self.specs.__dict__,
            "bom": [material.__dict__ for material in self.bom],
            "assets": self.assets.__dict__
        }
