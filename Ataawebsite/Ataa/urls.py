from django.urls import path
from .views import *
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/update/<int:pk>/', UpdateUserView.as_view(), name='update-user'),
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('add-item/', ItemCreateView.as_view(), name='add_item'),
    path('add-category/', CategoryCreateView.as_view(), name='add-category'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/details/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('addCart/', CartAddView.as_view(), name='cart-add'),
    path('cart/<int:pk>/delete/', CartDeleteView.as_view(), name='cart-delete'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/add/', OrderCreateView.as_view(), name='order-add'),

]
