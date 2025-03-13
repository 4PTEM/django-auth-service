from django.urls import path
from .views import SignUpView, SignInView, AuthView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),  # Add trailing slash
    path('signin/', SignInView.as_view(), name='signin'),  # Add trailing slash
    path('auth/', AuthView.as_view(), name='auth'),        # Add trailing slash
]
