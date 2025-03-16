from django.urls import path
from .views import SignUpView, SignInView, AuthView

urlpatterns = [
    path('auth-service-api/signup/', SignUpView.as_view(), name='signup'),  # Add trailing slash
    path('auth-service-api/signin/', SignInView.as_view(), name='signin'),  # Add trailing slash
    path('auth-service-api/auth/', AuthView.as_view(), name='auth'),        # Add trailing slash
]
