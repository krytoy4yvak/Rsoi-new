import json


class User:
    def __init__(self, user_id, prod_ids, name, admin):
        self.id = user_id
        self.prod_ids = prod_ids
        self.name = name
        self.admin = admin

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        else:
            return self.id == other.id and self.prod_ids == other.prod_ids and self.name == other.name and \
                   self.admin == other.admin

    def to_json(self):
        dictr = {'user_id': str(self.id), 'prod_ids': self.prod_ids, 'name': self.name, 'admin': self.admin}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return User(user_id=decoded_object['user_id'], prod_ids=decoded_object['prod_ids'],
                    name=decoded_object['name'], admin=decoded_object['admin'])