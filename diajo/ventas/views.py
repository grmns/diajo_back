# ventas/views.py

from rest_framework import viewsets
from .models import Venta, Cliente, Vendedor
from .serializers import VentaSerializer, ClienteSerializer, VendedorSerializer
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.db import DatabaseError



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    # Si el token es válido, llegará a este punto
    return Response({"message": "Token is valid"})


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    @action(detail=True, methods=['post'])
    def anular(self, request, pk=None):
        venta = self.get_object()
        venta.ANULADO = True
        venta.save()
        return Response({'status': 'venta anulada'}, status=status.HTTP_200_OK)


class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
