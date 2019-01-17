import json


class Prod:
    def __init__(self, prod_id, mag_id, cell):
        self.id = prod_id
        self.mag_id = mag_id
        self.cell = cell

    def __eq__(self, other):
        if not isinstance(other, Prod):
            return False
        else:
            return self.id == other.id and self.mag_id == other.mag_id and self.cell == other.cell

    def to_json(self):
        dictr = {'prod_id': str(self.id), 'mag_id': self.mag_id, 'cell': self.cell}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Prod(prod_id=decoded_object["prod_id"], mag_id=decoded_object["mag_id"],
                      cell=decoded_object["cell"])