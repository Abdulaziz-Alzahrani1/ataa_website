from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import logout
from .serializers import CustomUserCreationSerializer, LoginSerializer, CustomUserSerializer, ItemSerializer
from .models import CustomUser, Item
from django.shortcuts import render
from .models import Category, Cart
from .serializers import CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CartSerializer

class CartAddView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request
        })
        return context
    

class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the items in the cart
        for the currently authenticated user.
        """
        user = self.request.user
        return Cart.objects.filter(CustomUser=user)

class CartDeleteView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure that only items that belong to the authenticated user can be deleted.
        """
        user = self.request.user
        return Cart.objects.filter(CustomUser=user)


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(CustomUser=self.request.user)

class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserCreationSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'status': 'success', 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = CustomUser.objects.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj


class DeleteUserView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        print("Request method:", request.method)  # Log the request method
        user = self.get_object()
        if request.user != user and not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to delete this user.")
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
