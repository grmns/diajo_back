from django.urls import path, include
from .views import crear_compra
from rest_framework.routers import DefaultRouter
from .views import CompraViewSet, ProveedorViewSet, CuotaViewSet
from .views import LoginView, LogoutView
from .views import verify_token



router = DefaultRouter()
router.register(r'compras', CompraViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'cuotas', CuotaViewSet)

urlpatterns = [
    path('api/compras/crear/', crear_compra, name='crear_compra'),
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/verify_token/', verify_token, name='verify_token'),
]
