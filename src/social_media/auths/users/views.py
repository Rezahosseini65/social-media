from django.db import transaction
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import InputUserRegisterSerializer,OutputUserRegisterSerializer, UserLoginSerializer

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


class UserLoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success':'User logged in successfully.',
                    'refresh':str(refresh),
                    'access':str(refresh.access_token),

                    },
                   status=status.HTTP_200_OK
                )
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

