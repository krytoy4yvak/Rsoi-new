import unittest
import jsonpickle
import requests
from config import current_config
from kassir.domain.kassir import Kassir


class TestKassirCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'name': 'test', 'razryad': 'test', 'year': 30}
        res = requests.post(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        kassir = Kassir.from_json(res.content)
        requests.delete(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH + "/%s" % str(kassir.id))


class TestKassirResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                           "/5bfbacaf102bd238e0238fa5")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                           "/5bd0a513af")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'name': 'test', 'razryad': 'test', 'year': 30}
        res = requests.post(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        kassir = Kassir.from_json(res.content)
        res = requests.delete(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                              "/%s" % str(kassir.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH +
                              "/5bd8ad1daf13c7")
        self.assertEqual(res.status_code, 404)


class TestKassirListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.KASSIR_SERVICE_URL + current_config.KASSIR_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
