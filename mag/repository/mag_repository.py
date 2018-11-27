from flask_mongoalchemy import MongoAlchemy
from mag import app
from mag.domain.mag import Mag
import jsonpickle


db = MongoAlchemy(app)


class Mags(db.Document):
    kassir_id = db.ObjectIdField()
    date_time = db.StringField()
    col = db.StringField()


class MagRepository:
    def create(self, kassir_id, date_time, number_of_col):
        col = []
        for i in range(number_of_col):
            col.append(True)
        mag = Mags(kassir_id=kassir_id, date_time=date_time, col=jsonpickle.encode(col))
        mag.save()
        return mag.mongo_id

    def get(self, mag_id):
        if self.exists(mag_id):
            mag = Mags.query.get(mag_id)
            col = jsonpickle.decode(mag.col)
            return Mag(mag_id=mag.mongo_id, kassir_id=mag.kassir_id, date_time=mag.date_time, col=col)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        mags = []
        mags_paginated = Mags.query.paginate(page=page_number, per_page=page_size)
        for mag in mags_paginated.items:
            col = jsonpickle.decode(mag.col)
            mags.append(Mag(mag_id=mag.mongo_id, kassir_id=mag.kassir_id, date_time=mag.date_time,
                                  col=col))
        return mags

    def delete(self, mag_id):
        if self.exists(mag_id):
            mag = Mags.query.get(mag_id)
            mag.remove()

    def get_a_seat(self, mag_id, prod_col):
        if self.exists(mag_id):
            mag = Mags.query.get(mag_id)
            col = jsonpickle.decode(mag.col)
            if (len(col) >= prod_col) and (prod_col > 0) and (col[prod_col-1] == True):
                col[prod_col-1] = False
                mag.col = jsonpickle.encode(col)
                mag.save()
                return True
            else:
                return False
        else:
            return None

    def free_a_seat(self, mag_id, prod_col):
        if self.exists(mag_id):
            mag = Mags.query.get(mag_id)
            col = jsonpickle.decode(mag.col)
            if (len(col) >= prod_col) and (prod_col > 0) and (col[prod_col - 1] == False):
                col[prod_col-1] = True
                mag.col = jsonpickle.encode(col)
                mag.save()
                return True
            else:
                return False
        else:
            return None

    def exists(self, mag_id):
        result = Mags.query.get(mag_id)
        return result is not None