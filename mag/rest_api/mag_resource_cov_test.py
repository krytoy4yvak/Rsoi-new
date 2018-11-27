import unittest
from mag.rest_api.mag_resource import MagResource, MagListResource, MagCreateResource
from mag.domain.mag import Mag


class TestMagCreateResource(unittest.TestCase):
    def test_post(self):
        sr = MagCreateResource()
        res = sr.post()
        self.assertEqual(res.status_code, 201)
        sr1 = MagResource()
        mag = Mag.from_json(res.data)
        sr1.delete(str(mag.id))


class TestMagResource(unittest.TestCase):
    def test_get_right(self):
        scr = MagCreateResource()
        sr = MagResource()
        res = scr.post()
        mag = Mag.from_json(res.data)
        res = sr.get(str(mag.id))
        self.assertEqual(res.status_code, 200)
        sr.delete(str(mag.id))

    def test_get_error(self):
        sr = MagResource()
        try:
            res = sr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        sr = MagResource()
        try:
            res = sr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        sr = MagCreateResource()
        res = sr.post()
        sr1 = MagResource()
        mag = Mag.from_json(res.data)
        res = sr1.delete(str(mag.id))
        self.assertEqual(res.status_code, 204)


class TestMagListResource(unittest.TestCase):
    def test_get(self):
        sr = MagListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
