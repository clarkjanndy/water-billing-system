from django.http import JsonResponse
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)

from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count

from base.models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserList(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    
    serializer_class = CustomUserSerializer
