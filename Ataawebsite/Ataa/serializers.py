from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Item , Category,Cart
from .serializers import CartSerializer

class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class CartAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        item_id = data.get('item')
        quantity = data.get('quantity', 1)
        item = Item.objects.get(id=item_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, item=item, defaults={'quantity': quantity})

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            cart_item = Cart.objects.get(pk=pk, user=request.user)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
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
