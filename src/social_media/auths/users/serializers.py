from django.core.validators import MinLengthValidator

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .validators import number_validator, letter_validator


class InputUserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True,required=True,
        validators=[
            number_validator,
            letter_validator,
            MinLengthValidator(limit_value=8)
        ]
    )
    confirm_password = serializers.CharField()

    def validate_email(self, value:str)->str:
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("email Already exists")
        return value

    def validate(self, data:dict)->dict:
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(**validated_data)
        return user


class OutputUserRegisterSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'tokens')

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, write_only=True, required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)


