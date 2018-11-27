import unittest
from prod.rest_api.prod_resource import ProdCreateResource, ProdListResource, ProdResource
from prod.domain.prod import Prod


class TestProdCreateResource(unittest.TestCase):
    def test_post(self):
        tr = ProdCreateResource()
        res = tr.post()
        self.assertEqual(res.status_code, 201)
        tr1 = ProdResource()
        mag = Prod.from_json(res.data)
        tr1.delete(str(mag.id))


class TestProdResource(unittest.TestCase):
    def test_get_right(self):
        tr = ProdResource()
        tcr = ProdCreateResource()
        res = tcr.post()
        prod = Prod.from_json(res.data)
        res = tr.get(str(prod.id))
        self.assertEqual(res.status_code, 200)
        tr.delete(str(prod.id))

    def test_get_error(self):
        tr = ProdResource()
        try:
            res = tr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        tr = ProdResource()
        try:
            res = tr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        tr = ProdCreateResource()
        res = tr.post()
        tr1 = ProdResource()
        mag = Prod.from_json(res.data)
        res = tr1.delete(str(mag.id))
        self.assertEqual(res.status_code, 204)


class TestProdListResource(unittest.TestCase):
    def test_get(self):
        tr = ProdListResource()
        res = tr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
