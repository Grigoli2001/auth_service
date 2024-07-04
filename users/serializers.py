from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'type')
        extra_kwargs = {
                        'password': {
                        'write_only': True,
                        'required': True,
                        'validators': [password_validation.validate_password]
                        },
                        'email': {
                        'required': True,
                        'validators': [UniqueValidator(queryset=User.objects.all(),message='A user with that email already exists.')]
                        },
            }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            type=validated_data['type']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Update the last_login field
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return token