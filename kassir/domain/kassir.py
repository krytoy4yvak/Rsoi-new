import json


class Kassir:
    def __init__(self, kassir_id, name, razryad, year):
        self.id = kassir_id
        self.name = name
        self.razryad = razryad
        self.year = year

    def __eq__(self, other):
        if not isinstance(other, Kassir):
            return False
        else:
            return self.id == other.id and self.name == other.name and self.year == other.year and \
                   self.razryad == other.razryad

    def to_json(self):
        dictr = {'kassir_id': str(self.id), 'name': self.name, 'year': self.year, 'razryad': self.razryad}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Kassir(kassir_id=decoded_object["kassir_id"], name=decoded_object["name"],
                     razryad=decoded_object["razryad"], year=decoded_object["year"])
