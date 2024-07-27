from django.urls import path
from .views import RegisterView, UserListView, LoginView, DeleteUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
]
