from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Item, Category, Cart, Order

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('CustomUser',)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        return Cart.objects.create(CustomUser=user, **validated_data)

class CustomUserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type', 'password')
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
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False}
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.user_type = validated_data.get('user_type', instance.user_type)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid email or password')
        return {'user': user}

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('CustomUser',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
