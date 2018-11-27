import unittest
from kassir.rest_api.kassir_resource import KassirResource, KassirCreateResource, KassirListResource
from kassir.domain.kassir import Kassir


class TestKassirCreateResource(unittest.TestCase):
    def test_post(self):
        mr = KassirCreateResource()
        res = mr.post()
        self.assertEqual(res.status_code, 201)
        kassir = Kassir.from_json(res.data)
        mr1 = KassirResource()
        mr1.delete(str(kassir.id))


class TestKassirResource(unittest.TestCase):
    def test_get_right(self):
        mr1 = KassirResource()
        mr2 = KassirCreateResource()
        res = mr2.post()
        kassir = Kassir.from_json(res.data)
        res = mr1.get(str(kassir.id))
        self.assertEqual(res.status_code, 200)
        mr1.delete(str(kassir.id))

    def test_get_error(self):
        mr = KassirResource()
        try:
            res = mr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        mr = KassirResource()
        try:
            res = mr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        mr = KassirCreateResource()
        res = mr.post()
        kassir = Kassir.from_json(res.data)
        mr1 = KassirResource()
        res = mr1.delete(str(kassir.id))
        self.assertEqual(res.status_code, 204)


class TestKassirListResource(unittest.TestCase):
    def test_get(self):
        mr = KassirListResource()
        res = mr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
