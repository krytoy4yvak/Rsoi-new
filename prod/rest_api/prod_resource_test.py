import unittest
import jsonpickle
import requests
from config import current_config
from prod.domain.prod import Prod


class TestProdCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'mag_id': '5bfbb05b102bd23cdc85f75a', 'prod_col': 2}
        res = requests.post(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        prod = Prod.from_json(res.content)
        requests.delete(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                        "/%s" % str(prod.id))


class TestProdResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                           "/5bfbb084102bd2164418af43")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                           "/5bd0a351")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'mag_id': '5bfbb05b102bd23cdc85f75a', 'prod_col': 2}
        res = requests.post(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        prod = Prod.from_json(res.content)
        res = requests.delete(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH +
                              "/%s" % prod.id)
        self.assertEqual(res.status_code, 204)


class TestProdListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.PROD_SERVICE_URL + current_config.PROD_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
