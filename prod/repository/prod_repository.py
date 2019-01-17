from flask_mongoalchemy import MongoAlchemy
from prod import app
from prod.domain.prod import Prod


db = MongoAlchemy(app)


class Prods(db.Document):
    mag_id = db.StringField()
    cell = db.IntField()


class ProdRepository:
    def create(self, mag_id, cell):
        prod = Prods(mag_id=mag_id, cell=cell)
        prod.save()
        return prod.mongo_id

    def get(self, prod_id):
        if self.exists(prod_id):
            prod = Prods.query.get(prod_id)
            return Prod(prod_id=prod.mongo_id, mag_id=prod.mag_id, cell=prod.cell)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        prods = []
        prods_paged = Prods.query.paginate(page=page_number, per_page=page_size)
        for prod in prods_paged.items:
            prods.append(Prod(prod_id=prod.mongo_id, mag_id=prod.mag_id,
                                  cell=prod.cell))
        is_prev_num = (prods_paged.prev_num > 0)
        is_next_num = (prods_paged.next_num <= prods_paged.pages)
        return prods, is_prev_num, is_next_num

    def delete(self, prod_id):
        if self.exists(prod_id):
            prod = Prods.query.get(prod_id)
            prod.remove()

    def exists(self, prod_id):
        result = Prods.query.get(prod_id)
        return result is not None