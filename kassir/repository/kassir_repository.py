from flask_mongoalchemy import MongoAlchemy
from kassir import app
from kassir.domain.kassir import Kassir


db = MongoAlchemy(app)


class Kassirs(db.Document):
    name = db.StringField()
    stage = db.StringField()
    year = db.IntField()


class KassirRepository:
    def create(self, name, stage, year):
        kassir = Kassirs(name=name, stage=stage, year=year)
        kassir.save()
        return kassir.mongo_id

    def get(self, kassir_id):
        if self.exists(kassir_id):
            kassir = Kassirs.query.get(kassir_id)
            return Kassir(kassir_id=kassir.mongo_id, name=kassir.name, stage=kassir.stage,
                                           year=kassir.year)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        kassirs = []
        kassirs_paginated = Kassirs.query.paginate(page=page_number, per_page=page_size)
        for kassir in kassirs_paginated.items:
            kassirs.append(Kassir(kassir_id=kassir.mongo_id, name=kassir.name, stage=kassir.stage,
                                year=kassir.year))
        is_prev_num = (kassirs_paginated.prev_num > 0)
        is_next_num = (kassirs_paginated.next_num <= kassirs_paginated.pages)
        return kassirs, is_prev_num, is_next_num

    def delete(self, kassir_id):
        if self.exists(kassir_id):
            kassir = Kassirs.query.get(kassir_id)
            kassir.remove()

    def exists(self, kassir_id):
        result = Kassirs.query.get(kassir_id)
        return result is not None