import json

class User:
    def __init__(self, user_id, prod_ids, l_name, p_name):
        self.id = user_id
        self.prod_ids = prod_ids
        self.l_name = l_name
        self.p_name = p_name

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        else:
            return self.id == other.id and self.prod_ids == other.prod_ids and self.l_name == other.l_name and \
                   self.p_name == other.p_name

    def to_json(self):
        dictr = {'user_id': str(self.id), 'prod_ids': self.prod_ids, 'l_name': self.l_name, 'p_name': self.p_name}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return User(user_id=decoded_object['user_id'], prod_ids=decoded_object['prod_ids'],
                    l_name=decoded_object['l_name'], p_name=decoded_object['p_name'])