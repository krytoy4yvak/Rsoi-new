from flask_mongoalchemy import MongoAlchemy
from prod import app
from prod.domain.prod import Prod


db = MongoAlchemy(app)


class Prods(db.Document):
    mag_id = db.StringField()
    prod_col = db.IntField()


class ProdRepository:
    def create(self, mag_id, prod_col):
        prod = Prods(mag_id=mag_id, prod_col=prod_col)
        prod.save()
        return prod.mongo_id

    def get(self, prod_id):
        if self.exists(prod_id):
            prod = Prods.query.get(prod_id)
            return Prod(prod_id=prod.mongo_id, mag_id=prod.mag_id, prod_col=prod.prod_col)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        prods = []
        prods_paged = Prods.query.paginate(page=page_number, per_page=page_size)
        for prod in prods_paged.items:
            prods.append(Prod(prod_id=prod.mongo_id, mag_id=prod.mag_id,
                                  prod_col=prod.prod_col))
        return prods

    def delete(self, prod_id):
        if self.exists(prod_id):
            prod = Prods.query.get(prod_id)
            prod.remove()

    def exists(self, prod_id):
        result = Prods.query.get(prod_id)
        return result is not None