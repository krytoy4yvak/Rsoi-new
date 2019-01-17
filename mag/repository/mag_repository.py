from flask_mongoalchemy import MongoAlchemy
from mag import app
from mag.domain.mag import Mag
import jsonpickle


db = MongoAlchemy(app)


class Mags(db.Document):
    kassir_id = db.ObjectIdField()
    date_time = db.StringField()
    seats = db.StringField()


class MagRepository:
    def create(self, kassir_id, date_time, number_of_seats):
        seats = []
        for i in range(number_of_seats):
            seats.append(True)
        mag = Mags(kassir_id=kassir_id, date_time=date_time, seats=jsonpickle.encode(seats))
        mag.save()
        return mag.mongo_id

    def get(self, mag_id):
        if self.exists(mag_id):
            mag = Mags.query.get(mag_id)
            seats = jsonpickle.decode(mag.seats)
            return Mag(mag_id=mag.mongo_id, kassir_id=mag.kassir_id, date_time=mag.date_time, seats=seats)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        mags = []
        mags_paginated = Mags.query.paginate(page=page_number, per_page=page_size)
        for mag in mags_paginated.items:
            seats = jsonpickle.decode(mag.seats)
            mags.append(Mag(mag_id=mag.mongo_id, kassir_id=mag.kassir_id, date_time=mag.date_time,
                                  seats=seats))
        is_prev_num = (mags_paginated.prev_num > 0)
        is_next_num = (mags_paginated.next_num <= mags_paginated.pages)
        return mags, is_prev_num, is_next_num

    def delete(self, mag_id):
        if self.exists(mag_id):
            mag = Mags.query.get(mag_id)
            mag.remove()

    def get_a_seat(self, mag_id, cell):
        if self.exists(mag_id):
            mag = Mags.query.get(mag_id)
            seats = jsonpickle.decode(mag.seats)
            if (len(seats) >= cell) and (cell > 0) and (seats[cell-1] == True):
                seats[cell-1] = False
                mag.seats = jsonpickle.encode(seats)
                mag.save()
                return True
            else:
                return False
        else:
            return None

    def free_a_seat(self, mag_id, cell):
        if self.exists(mag_id):
            mag = Mags.query.get(mag_id)
            seats = jsonpickle.decode(mag.seats)
            if (len(seats) >= cell) and (cell > 0) and (seats[cell - 1] == False):
                seats[cell-1] = True
                mag.seats = jsonpickle.encode(seats)
                mag.save()
                return True
            else:
                return False
        else:
            return None

    def exists(self, mag_id):
        result = Mags.query.get(mag_id)
        return result is not None