import os


class Config:
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = "kiameiieiihig#$%%%^(()_udavhgusk$%#%^******"

    DB_HOST = os.getenv('DB_HOST')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True

    DB_HOST = os.getenv('DB_TEST_HOST')
    DB_USERNAME = os.getenv('DB_TEST_USERNAME')
    DB_PASSWORD = os.getenv('DB_TEST_PASSWORD')
    DB_NAME = os.getenv('DB_TEST_NAME')


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
