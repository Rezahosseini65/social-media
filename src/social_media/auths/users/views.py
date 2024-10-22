from django.db import transaction

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import InputUserRegisterSerializer,OutputUserRegisterSerializer

# Create your views here.


class UserRegisterApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InputUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                output_serializer = OutputUserRegisterSerializer(user)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)