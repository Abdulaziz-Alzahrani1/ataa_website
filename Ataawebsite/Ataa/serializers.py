from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'user_type', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_user_type(self, value):
        if value not in dict(CustomUser.USER_TYPE_CHOICES).keys():
            raise serializers.ValidationError('Invalid user type')
        return value

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid email or password')
        return {'user': user}
