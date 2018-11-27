import unittest
import jsonpickle
import requests
from config import current_config
from mag.domain.mag import Mag
from kassir.domain.kassir import Kassir
from prod.domain.prod import Prod


class TestGatewayProdResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.PROD_SERVICE_PATH
                           + "/5bfbb084102bd2164418af43")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.PROD_SERVICE_PATH
                           + "/5bd8842")
        self.assertEqual(res.status_code, 404)


class TestGatewayProdListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.PROD_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.PROD_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayMagResource(unittest.TestCase):
    # def test_get_right(self):
    #     res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MAG_SERVICE_PATH
    #                        + "/5bfbb05b102bd23cdc85f75a")
    #     self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.PROD_SERVICE_PATH
                           + "/5bd0aa41af13")
        self.assertNotEqual(res.status_code, 200)


class TestGatewayMagCreateResource(unittest.TestCase):
    def test_post_right(self):
        payload = {'kassir_id': '5bfbacaf102bd238e0238fa5', 'datetime': '22.11.2018_10:15', 'col':100}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MAG_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        mag = Mag.from_json(res.content)
        requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MAG_SERVICE_PATH +
                        "/%s" % str(mag.id))

    def test_post_error(self):
        payload = {'kassir_id': '5bfbacaf102bd238e0238fa5', 'datetime': '22.11.2018_10:15', 'col':'100'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.PROD_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewayMagListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.MAG_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.MAG_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayKassirResource(unittest.TestCase):
    # def test_get_right(self):
    #     res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.KASSIR_SERVICE_PATH
    #                        + "/5bfbacaf102bd238e0238fa5")
    #     self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.KASSIR_SERVICE_PATH
                           + "/5bd0a513")
        self.assertNotEqual(res.status_code, 200)

    # def test_delete_right(self):
    #     payload = {'name': 'test', 'razryad': 'test', 'year': 30}
    #     res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
    #                         current_config.KASSIR_SERVICE_PATH + current_config.CREATE_PATH,
    #                         data=jsonpickle.encode(payload))
    #     kassir = Kassir.from_json(res.content)
    #     res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
    #                           current_config.KASSIR_SERVICE_PATH + "/%s" % str(kassir.id))
    #     self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              current_config.KASSIR_SERVICE_PATH + "/0")
        self.assertNotEqual(res.status_code, 204)


class TestGatewayKassirCreateResource(unittest.TestCase):
    def test_post_right(self):
        payload = {'name': 'test', 'razryad': 'test', 'year': 30}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.KASSIR_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        kassir = Kassir.from_json(res.content)
        requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.KASSIR_SERVICE_PATH +
                        "/%s" % str(kassir.id))

    def test_post_error(self):
        payload = {'name': 'test', 'razryad': 'test', 'year': "0"}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.KASSIR_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewayKassirListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.KASSIR_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.KASSIR_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayUserResource(unittest.TestCase):
    # def test_get_right(self):
    #     res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.USER_SERVICE_PATH
    #                        + "/5bd0a351af13c713737dae92")
    #     self.assertEqual(res.status_code, 200)

    def test_get_with_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.USER_SERVICE_PATH
                           + "/5bd0")
        self.assertNotEqual(res.status_code, 200)


class TestGatewayUserListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.USER_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.USER_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayBuyProd(unittest.TestCase):
    # def test_post_right(self):
    #     payload = {'mag_id': '5bd897f8af13c78fe908cb98', 'seat_number': 6}
    #     res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/prods/buy',
    #                         data=jsonpickle.encode(payload))
    #     self.assertEqual(res.status_code, 201)
    #     prod = Prod.from_json(res.content)
    #     requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
    #                     '/prods/return/%s' % str(prod.id))

    def test_post_error(self):
        payload = {'mag_id': '5bd897f8', 'seat_number': 2}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/prods/buy',
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewayReturnProd(unittest.TestCase):
    # def test_delete_right(self):
    #     payload = {'mag_id': '5bd897f8af13c78fe908cb98', 'seat_number': 6}
    #     res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/prods/buy',
    #                         data=jsonpickle.encode(payload))
    #     prod = Prod.from_json(res.content)
    #     res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
    #                           '/prods/return/%s' % str(prod.id))
    #     self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              '/return_prod/5bd8a540af13')
        self.assertNotEqual(res.status_code, 204)


if __name__ == '__main__':
    unittest.main()
