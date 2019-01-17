class Config(object):
    DEBUG = False
    TESTING = False
    GATEWAY_PATH = "/gateway/api"

    CREATE_PATH = "/create"

    KASSIR_SERVICE_PATH = "/kassirs"

    MAG_SERVICE_PATH = "/mags"

    PROD_SERVICE_PATH = "/prods"

    USER_SERVICE_PATH = "/users"

    GET_TOKEN_URL_PATH = "/auth/token"

    PORT = 5000
    GATEWAY_URL = "http://127.0.0.1:5000"
    KASSIR_SERVICE_URL = "http://127.0.0.1:5001"
    MAG_SERVICE_URL = "http://127.0.0.1:5002"
    PROD_SERVICE_URL = "http://127.0.0.1:5003"
    USER_SERVICE_URL = "http://127.0.0.1:5004"


current_config = Config()