import json


class Mag:
    def __init__(self, mag_id, kassir_id, date_time, seats):
        self.id = mag_id
        self.kassir_id = kassir_id
        self.date_time = date_time
        self.seats = seats

    def __eq__(self, other):
        if not isinstance(other, Mag):
            return False
        else:
            return self.id == other.id and self.kassir_id == other.kassir_id and self.date_time == other.date_time and \
                   self.seats == other.seats

    def to_json(self):
        dictr = {'mag_id': str(self.id), 'kassir_id': str(self.kassir_id), 'datetime': self.date_time,
                 'seats': self.seats}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Mag(mag_id=decoded_object["mag_id"], kassir_id=decoded_object["kassir_id"],
                      date_time=decoded_object["datetime"], seats=decoded_object["seats"])