import json


class Prod:
    def __init__(self, prod_id, mag_id, prod_col):
        self.id = prod_id
        self.mag_id = mag_id
        self.prod_col = prod_col

    def __eq__(self, other):
        if not isinstance(other, Prod):
            return False
        else:
            return self.id == other.id and self.mag_id == other.mag_id and self.prod_col == other.prod_col

    def to_json(self):
        dictr = {'prod_id': str(self.id), 'mag_id': self.mag_id, 'prod_col': self.prod_col}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Prod(prod_id=decoded_object["prod_id"], mag_id=decoded_object["mag_id"],
                      prod_col=decoded_object["prod_col"])