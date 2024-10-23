from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.UserRegisterApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
]