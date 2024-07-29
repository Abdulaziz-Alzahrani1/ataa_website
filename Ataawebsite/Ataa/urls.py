from django.urls import path
from .views import CartListView, CartAddView, CartDeleteView,ItemListView,CategoryCreateView,RegisterView, UserListView, LoginView, LogoutView, DeleteUserView, UpdateUserView ,  ItemCreateView

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
    path('cart/', CartListView.as_view(), name='cart-list'),
    path('cart/add/', CartAddView.as_view(), name='cart-add'),
    path('cart/delete/<int:pk>/', CartDeleteView.as_view(), name='cart-delete'),
]
