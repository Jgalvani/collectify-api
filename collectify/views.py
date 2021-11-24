from rest_framework import authtoken, permissions, viewsets

from .models import CarHasColor, Color, Car, User
from .serializers import ColorSerializer, CarSerializer, UserSerializer


# Create your views here.
class ColorViewSet(viewsets.ModelViewSet):
    """
    List, create, retrieve, update and delete colors
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.IsAuthenticated]


class CarViewSet(viewsets.ModelViewSet):
    """
    List, create, retrieve, update and delete cars
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    List, create, retrieve, update and delete users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
