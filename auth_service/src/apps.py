from mongoengine import connect
from django.apps import AppConfig
import os
from dotenv import load_dotenv

class AuthConfig(AppConfig):
    name = 'src'

    def ready(self):
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))

        load_dotenv()

        username = os.getenv('MONGODB_USERNAME')
        password = os.getenv('MONGODB_PASSWORD')
        port = int(os.getenv('MONGODB_PORT'))
        host = os.getenv('MONGODB_HOST')
        db = os.getenv('MONGODB_DBNAME')

        print(f"Connecting to MongoDB at {host}:{port} as {username} with password {password} for database {db}")

        connect(host=f"mongodb://{username}:{password}@{host}:{port}/{db}?authSource=admin")

