from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('create/user/', views.createUser),
    path('login/', views.loginUser),
    path('user/<int:id>/', views.getUserDetails),
    path('user/<int:id>/update/', views.updateUserDetails),
    path('logout/', views.logoutUser),
]