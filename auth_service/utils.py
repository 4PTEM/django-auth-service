import jwt
import datetime
from django.conf import settings

SECRET_KEY = 'mysecret'

def generate_jwt(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'user_id': str(user_id),
        'exp': expiration_time
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def validate_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
