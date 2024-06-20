# ventas/urls.py

from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, VentaViewSet, VendedorViewSet, verify_token
from .views import LoginView, LogoutView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'vendedores', VendedorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/verify_token/', verify_token, name='verify_token'),
]
