import unittest
from prod.repository.prod_repository import ProdRepository
from prod.domain.prod import Prod
from flask_mongoalchemy import fields


class TestProdRepository(unittest.TestCase):
    def test_create(self):
        rep = ProdRepository()
        id1 = rep.create('5bd897f8af13c78fe908cb98', 2)
        id2 = rep.create('5bd897f8af13c78fe908cb98', 2)
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    def test_get_right(self):
        rep = ProdRepository()
        prod_id = rep.create(mag_id='5bfbb05b102bd23cdc85f75a', prod_col=1)
        prod1 = rep.get(prod_id)
        prod2 = Prod(prod_id=fields.ObjectId(prod_id), mag_id='5bfbb05b102bd23cdc85f75a', prod_col=1)
        self.assertEqual(prod1, prod2)
        rep.delete(prod_id)

    def test_get_error(self):
        rep = ProdRepository()
        prod = rep.get('5bd89fd9')
        self.assertIsNone(prod)

    def test_read_paginated(self):
        rep = ProdRepository()
        prods = rep.read_paginated(1, 5)
        self.assertLessEqual(len(prods), 5)

    def test_delete_existed(self):
        rep = ProdRepository()
        id1 = rep.create('5bd897f8af13c78fe908cb98', 2)
        rep.delete(id1)
        self.assertFalse(rep.exists(id1))

    def test_exists_true(self):
        rep = ProdRepository()
        prod_id = rep.create(mag_id='5bfbb05b102bd23cdc85f75a', prod_col=1)
        boolean = rep.exists(prod_id)
        self.assertTrue(boolean)
        rep.delete(prod_id)

    def test_exists_false(self):
        rep = ProdRepository()
        boolean = rep.exists('5bd8ad1daf')
        self.assertFalse(boolean)


if __name__ == '__main__':
    unittest.main()
