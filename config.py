# config.py
class Config:
    DEBUG = True
    NEWS_API_KEY = 'pub_48828138c1a7fd2c74b3ce209941d0767481c'
    BASE_URL = 'https://newsdata.io/api/1/news'

class ProductionConfig:
    DEBUG = False
    # Production specific configurations

class DevelopmentConfig(Config):
    DEBUG = True
    # Development specific configurations

class TestingConfig(Config):
    TESTING = True
    # Testing specific configurations

