class Config(object):
    DEBUG = False
    TESTING = False
    GATEWAY_SERVICE_PATH = "/gateway/api"

    CREATE_PATH = "/create"

    KASSIR_SERVICE_PATH = "/kassirs"
    KASSIR_URL_PATH = "/<kassir_id>"

    MAG_SERVICE_PATH = "/mags"
    MAG_URL_PATH = "/<mag_id>"

    PROD_SERVICE_PATH = "/prods"
    PROD_URL_PATH = "/<prod_id>"

    USER_SERVICE_PATH = "/users"
    USER_URL_PATH = "/<user_id>"

    SECRET_KEY = "qwerty1234"

    GET_TOKEN_URL_PATH = "/auth/token"


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5005
    GUI_SERVICE_URL = "http://127.0.0.1:%d" % PORT
    GATEWAY_SERVICE_URL = "http://127.0.0.1:5000"


current_config = DevelopmentConfig()