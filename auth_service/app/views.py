import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from mongoengine.errors import NotUniqueError
from .models import User
from .utils import generate_jwt, validate_jwt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sign up endpoint
class SignUpView(View):
    @csrf_exempt
    def post(self, request):
        logger.info("Received sign-up request")
        
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request body")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        if not username or not email or not password:
            logger.warning("Missing required fields in sign-up request")
            return JsonResponse({"error": "Missing required fields"}, status=400)
        
        try:
            user = User(username=username, email=email, password=password)
            user.save()
            token = generate_jwt(user.id)
            logger.info(f"User {username} created successfully")
            return JsonResponse({"jwt": token}, status=201)
        except NotUniqueError:
            logger.warning(f"User {username} already exists")
            return JsonResponse({"error": "User already exists"}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error during sign-up: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)

# Sign in endpoint
class SignInView(View):
    @csrf_exempt
    def post(self, request):
        logger.info("Received sign-in request")
        
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request body")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        if not username or not password:
            logger.warning("Missing required fields in sign-in request")
            return JsonResponse({"error": "Missing required fields"}, status=400)
        
        user = User.objects(username=username, password=password).first()
        if user:
            token = generate_jwt(user.id)
            logger.info(f"User {username} authenticated successfully")
            return JsonResponse({"jwt": token}, status=200)
        else:
            logger.warning(f"Invalid credentials for username: {username}")
            return JsonResponse({"error": "Invalid credentials"}, status=401)

class AuthView(View):
    def get(self, request):
        logger.info("Received authentication request")
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("Authorization header missing")
            return JsonResponse({"error": "Authorization header missing"}, status=403)
        
        try:
            token = auth_header.split(" ")[1]
            payload = validate_jwt(token)
            
            if payload:
                user_id = payload.get('user_id')
                user = User.objects.get(id=user_id)
                
                logger.info(f"User {user_id} authenticated successfully")
                response = JsonResponse({"message": "Authenticated"}, status=200)
                response['X-USER-ROLE'] = user.role if hasattr(user, 'role') else 'user'
                response['Authorization'] = auth_header
                return response
            else:
                logger.warning("Invalid or expired token")
                return JsonResponse({"error": "Invalid or expired token"}, status=403)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return JsonResponse({"error": f"Authentication error: {str(e)}"}, status=403)
