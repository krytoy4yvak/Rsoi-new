import unittest
from kassir.repository.kassir_repository import KassirRepository
from kassir.domain.kassir import Kassir
from flask_mongoalchemy import fields


class TestKassirRepository(unittest.TestCase):
    def test_create(self):
        rep = KassirRepository()
        id1 = rep.create('a', 'a', 10)
        id2 = rep.create('a', 'a', 10)
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    def test_get_right(self):
        rep = KassirRepository()
        kassir_id = rep.create('a', 'a', 100)
        kassir1 = rep.get(kassir_id)
        kassir2 = Kassir(kassir_id=fields.ObjectId(kassir_id), name='a', razryad='a', year=100)
        self.assertEqual(kassir1, kassir2)
        rep.delete(kassir_id)

    def test_get_none(self):
        rep = KassirRepository()
        kassir = rep.get('5bd8ad')
        self.assertIsNone(kassir)

    def test_exists_true(self):
        rep = KassirRepository()
        kassir_id = rep.create('a', 'a', 100)
        boolean = rep.exists(kassir_id)
        self.assertTrue(boolean)
        rep.delete(kassir_id)

    def test_exists_false(self):
        rep = KassirRepository()
        boolean = rep.exists('5bd8ad1daf')
        self.assertFalse(boolean)

    def test_read_paginated(self):
        rep = KassirRepository()
        kassirs = rep.read_paginated(1, 5)
        self.assertLessEqual(len(kassirs), 5)

    def test_delete_existed(self):
        rep = KassirRepository()
        id1 = rep.create('a', 'a', 10)
        rep.delete(id1)
        self.assertFalse(rep.exists(id1))


if __name__ == '__main__':
    unittest.main()
