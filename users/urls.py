from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import PerfilView, LoginModifiedView, RegisterView

app_name = 'users'

urlpatterns = [
    path('<str:username>', PerfilView.as_view(), name='perfil'),
    path('login/', LoginModifiedView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="users:login"), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]