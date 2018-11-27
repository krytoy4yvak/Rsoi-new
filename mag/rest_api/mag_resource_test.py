import unittest
import jsonpickle
import requests
from config import current_config
from mag.domain.mag import Mag


class TestMagCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'kassir_id': '5bfbacaf102bd238e0238fa5', 'datetime': '10.10.2010', 'col': 30}
        res = requests.post(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        mag = Mag.from_json(res.content)
        requests.delete(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH + "/%s" % str(mag.id))


class TestMagResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                           "/5bfbb05b102bd23cdc85f75a")
        self.assertEqual(res.status_code, 200)

    def test_get_false(self):
        res = requests.get(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                           "/5bd897f8af")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'kassir_id': '5bfbacaf102bd238e0238fa5', 'datetime': '10.10.2010', 'col': 30}
        res = requests.post(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        mag = Mag.from_json(res.content)
        res = requests.delete(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                              "/%s" % str(mag.id))
        self.assertEqual(res.status_code, 204)

    def test_patch_buy_right(self):
        mag_id = '5bfbb05b102bd23cdc85f75a'
        payload = {'prod_col': 10, 'status': 'buy'}
        res = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                             "/5bfbb05b102bd23cdc85f75a", data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        payload['status'] = 'return'
        requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                       "/5bfbb05b102bd23cdc85f75a", data=jsonpickle.encode(payload))

    def test_patch_buy_error(self):
        mag_id = '5bfbb05b102bd23cdc85f75a'
        payload = {'prod_col': 1, 'status': 'buy'}
        res = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                             "/5bfbb05b102bd23cdc85f75a", data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)

    def test_patch_return_right(self):
        mag_id = '5bfbb05b102bd23cdc85f75a'
        payload = {'prod_col': 1, 'status': 'return'}
        res = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                             "/5bfbb05b102bd23cdc85f75a", data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        payload['status'] = 'buy'
        requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                       "/5bfbb05b102bd23cdc85f75a", data=jsonpickle.encode(payload))

    def test_patch_return_error(self):
        mag_id = '5bfbb05b102bd23cdc85f75a'
        payload = {'prod_col': 10, 'status': 'return'}
        res = requests.patch(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH +
                             "/5bfbb05b102bd23cdc85f75a", data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestMagListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.MAG_SERVICE_URL + current_config.MAG_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
