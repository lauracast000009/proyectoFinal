from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegistroView, LoginView, LogoutView, UsuarioViewSet, CambiarPasswordView
)

router = DefaultRouter()
router.register(r'admin/users', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('auth/register/', RegistroView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/password/change/', CambiarPasswordView.as_view(), name='password-change'),
    path('', include(router.urls)),
]
