from django.urls import path
from .views import RegisterView, UserListView, LoginView, LogoutView, DeleteUserView, UpdateUserView ,  ItemCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/update/<int:pk>/', UpdateUserView.as_view(), name='update-user'),
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('api/add-item/', ItemCreateView.as_view(), name='add_item'),
]
