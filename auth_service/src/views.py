from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from mongoengine.errors import NotUniqueError
from .models import User
from .utils import generate_jwt, validate_jwt
import json

# Sign up endpoint
class SignUpView(View):
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return JsonResponse({"error": "Missing required fields"}, status=400)
        
        try:
            user = User(username=username, email=email, password=password)
            user.save()
            token = generate_jwt(user.id)
            return JsonResponse({"jwt": token}, status=201)
        except NotUniqueError:
            return JsonResponse({"error": "User already exists"}, status=400)

# Sign in endpoint
class SignInView(View):
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({"error": "Missing required fields"}, status=400)
        
        user = User.objects(username=username, password=password).first()
        if user:
            token = generate_jwt(user.id)
            return JsonResponse({"jwt": token}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

class AuthView(View):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=403)
        
        try:
            token = auth_header.split(" ")[1]
            payload = validate_jwt(token)
            
            if payload:
                user_id = payload.get('user_id')
                user = User.objects.get(id=user_id)
                
                response = JsonResponse({"message": "Authenticated"}, status=200)
                
                response['X-USER-ROLE'] = user.role if hasattr(user, 'role') else 'user'
                response['Authorization'] = auth_header
                
                return response
            else:
                return JsonResponse({"error": "Invalid or expired token"}, status=403)
        except Exception as e:
            return JsonResponse({"error": f"Authentication error: {str(e)}"}, status=403)
