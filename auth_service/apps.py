from mongoengine import connect
from django.apps import AppConfig

class AuthConfig(AppConfig):
    name = 'auth_service'

    def ready(self):
        connect(db='auth_db', host='localhost', port=27017)
