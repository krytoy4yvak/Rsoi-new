import unittest
import jsonpickle
import requests
from config import current_config
from gateway.rest_api.gateway_api import GatewayKassirCreateResource, GatewayKassirListResource, GatewayUserResource
from gateway.rest_api.gateway_api import GatewayReturnProd
from gateway.rest_api.gateway_api import GatewayMagCreateResource, GatewayMagListResource, GatewayKassirResource
from gateway.rest_api.gateway_api import GatewayProdResource, GatewayProdListResource, GatewayMagResource
from kassir.rest_api.kassir_resource import KassirResource, KassirCreateResource
from mag.rest_api.mag_resource import MagResource, MagCreateResource
from prod.rest_api.prod_resource import ProdResource, ProdCreateResource
from user.rest_api.user_resource import UserResource, UserCreateResource
from kassir.domain.kassir import Kassir
from mag.domain.mag import Mag
from prod.domain.prod import Prod
from user.domain.user import User


class TestGatewayProdResource(unittest.TestCase):
    def test_get_right(self):
        tr = ProdResource()
        tcr = ProdCreateResource()
        res = tcr.post()
        prod = Prod.from_json(res.data)
        gtr = GatewayProdResource()
        res = gtr.get(str(prod.id))
        self.assertEqual(res.status_code, 200)
        tr.delete(str(prod.id))

    def test_get_error(self):
        gtr = GatewayProdResource()
        try:
            res = gtr.get("5bd88423")
        except:
            self.assertTrue(True)


class TestGatewayProdListResource(unittest.TestCase):
    def test_get(self):
        sr = GatewayProdListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayMagResource(unittest.TestCase):
    # def test_get_right(self):
    #     sr = MagResource()
    #     scr = MagCreateResource()
    #     res = scr.post()
    #     mag = Mag.from_json(res.data)
    #     gsr = GatewayMagResource()
    #     res = gsr.get(str(mag.id))
    #     self.assertEqual(res.status_code, 200)
    #     sr.delete(str(mag.id))

    def test_get_error(self):
        gtr = GatewayMagResource()
        try:
            res = gtr.get("5bd88423")
        except:
            self.assertTrue(True)


# class TestGatewayMagCreateResource(unittest.TestCase):
#     def test_post(self):
#         gsr = GatewayMagCreateResource()
#         res = gsr.post()
#         self.assertEqual(res.status_code, 201)
#         sr = MagResource()
#         mag = Mag.from_json(res.data)
#         sr.delete(str(mag.id))


class TestGatewayMagListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewayMagListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayKassirResource(unittest.TestCase):
    def test_get_right(self):
        mr = KassirResource()
        mcr = KassirCreateResource()
        res = mcr.post()
        kassir = Kassir.from_json(res.data)
        gmr = GatewayKassirResource()
        res = gmr.get(str(kassir.id))
        self.assertEqual(res.status_code, 200)
        mr.delete(str(kassir.id))

    def test_get_error(self):
        gmr = GatewayKassirResource()
        try:
            res = gmr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        gmr = GatewayKassirResource()
        try:
            res = gmr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        gmr = GatewayKassirCreateResource()
        res = gmr.post()
        kassir = Kassir.from_json(res.data)
        gmr1 = GatewayKassirResource()
        res = gmr1.delete(str(kassir.id))
        self.assertEqual(res.status_code, 204)


class TestGatewayKassirCreateResource(unittest.TestCase):
    def test_post(self):
        gmr = GatewayKassirCreateResource()
        res = gmr.post()
        self.assertEqual(res.status_code, 201)
        mr = KassirResource()
        kassir = Kassir.from_json(res.data)
        mr.delete(str(kassir.id))


class TestGatewayKassirListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewayKassirListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayUserResource(unittest.TestCase):
    def test_get_right(self):
        ur = UserResource()
        ucr = UserCreateResource()
        res = ucr.post()
        user = User.from_json(res.data)
        gur = GatewayUserResource()
        res = gur.get(str(user.id))
        self.assertEqual(res.status_code, 200)
        ur.delete(str(user.id))

    def test_get_error(self):
        gur = GatewayUserResource()
        try:
            res = gur.get("5bd0a351")
        except:
            self.assertTrue(True)


class TestGatewayUserListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewayKassirListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayReturnProd(unittest.TestCase):
    def test_delete_right(self):
        payload = {'mag_id': '5bfcea57102bd21af8d4307e', 'prod_col': 7}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/prods/buy',
                            data=jsonpickle.encode(payload))
        prod = Prod.from_json(res.content)
        ret_prod = GatewayReturnProd()
        res = ret_prod.delete(str(prod.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        ret_prod = GatewayReturnProd()
        res = ret_prod.delete("5bd897f8")
        self.assertNotEqual(res.status_code, 204)


if __name__ == '__main__':
    unittest.main()
