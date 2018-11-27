from flask_mongoalchemy import MongoAlchemy
from user import app
from user.domain.user import User
import jsonpickle


db = MongoAlchemy(app)


class Users(db.Document):
    prod_ids = db.StringField()
    l_name = db.StringField()
    p_name = db.StringField()


class UserRepository:
    def create(self, l_name, p_name):
        prod_ids =['5bfbd9c7102bd21d84dee4b8','5bfbce18102bd21d84dee4b6','5bfcea74102bd227902276c0']
        user = Users(prod_ids=jsonpickle.encode(prod_ids), l_name=l_name, p_name=str(p_name))
        user.save()
        return user.mongo_id

    def get(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            prod_ids = jsonpickle.decode(user.prod_ids)
            return User(user_id=user.mongo_id, prod_ids=prod_ids, l_name=user.l_name, p_name=user.p_name)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        users = []
        users_paged = Users.query.paginate(page=page_number, per_page=page_size)

        for user in users_paged.items:
            prod_ids = jsonpickle.decode(user.prod_ids)
            users.append(User(user_id=user.mongo_id, prod_ids=prod_ids, l_name=user.l_name,
                              p_name=user.p_name))
        return users

    def delete(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            user.remove()

    def assign_prod(self, user_id, prod_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            prod_ids = jsonpickle.decode(user.prod_ids)
            prod_ids.append(prod_id)
            #prod_ids = user.prod_ids + tuple(str(prod_id))
            user.prod_ids = jsonpickle.encode(prod_ids)
            user.save()
            return True
        return False

    def remove_prod(self, user_id, prod_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            prod_ids = jsonpickle.decode(user.prod_ids)
            prod_ids.remove(prod_id)
            user.prod_ids = jsonpickle.encode(prod_ids)
            user.save()
            return True
        return False

    def exists(self, user_id):
        result = Users.query.get(user_id)
        return result is not None


