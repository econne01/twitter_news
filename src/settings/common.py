import os

class Settings(object):
    PROJECT_DIR = os.getcwd()

    DEBUG = True
    SECRET_KEY = '9a433844-b9cc-4cfe-8723-5167d4d8ec1a' # generated with uuid4

    STATIC_DIRECTORY = PROJECT_DIR + '/src/static'
    TEMPLATE_DIRECTORY = PROJECT_DIR + '/src/templates'
