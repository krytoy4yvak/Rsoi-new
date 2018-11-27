import unittest
from user.repository.user_repository import UserRepository
from user.domain.user import User
from flask_mongoalchemy import fields


class TestUserRepository(unittest.TestCase):
    def test_create(self):
        rep = UserRepository()
        id1 = rep.create('l_name', 'p_name')
        id2 = rep.create('l_name', 'p_name')
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    # def test_get_right(self):
    #     rep = UserRepository()
    #     user_id = rep.create('l_name', 'p_name')
    #     user1 = rep.get(user_id)
    #     user2 = User(user_id=fields.ObjectId(user_id), prod_ids=[], l_name='l_name', p_name='p_name')
    #     self.assertEqual(user1, user2)
    #     rep.delete(user_id)

    def test_get_error(self):
        rep = UserRepository()
        user = rep.get('5bd0a397')
        self.assertIsNone(user)

    def test_read_paginated(self):
        rep = UserRepository()
        users = rep.read_paginated(1, 5)
        self.assertLessEqual(len(users), 5)

    def test_delete_existed(self):
        rep = UserRepository()
        id1 = rep.create('l_name', 'p_name')
        rep.delete(id1)
        self.assertFalse(rep.exists(id1))

    def test_assign_ticket_true(self):
        rep = UserRepository()
        user_id = rep.create('l_name', 'p_name')
        boolean = rep.assign_prod(user_id, 'abc')
        self.assertTrue(boolean)
        rep.delete(user_id)

    def test_assign_ticket_false(self):
        rep = UserRepository()
        boolean = rep.assign_prod('5bd0a397', 'abc')
        self.assertFalse(boolean)

    def test_remove_ticket_true(self):
        rep = UserRepository()
        user_id = rep.create('l_name', 'p_name')
        rep.assign_prod(user_id, 'abc')
        boolean = rep.remove_prod(user_id, 'abc')
        self.assertTrue(boolean)
        rep.delete(user_id)

    def test_remove_ticket_false(self):
        rep = UserRepository()
        boolean = rep.remove_prod('5bd0a397', 'abc')
        self.assertFalse(boolean)

    def test_exists_true(self):
        rep = UserRepository()
        user_id = rep.create('l_name', 'p_name')
        boolean = rep.exists(user_id)
        self.assertTrue(boolean)
        rep.delete(user_id)

    def test_exists_false(self):
        rep = UserRepository()
        boolean = rep.exists('5bd8ad1daf')
        self.assertFalse(boolean)


if __name__ == '__main__':
    unittest.main()
