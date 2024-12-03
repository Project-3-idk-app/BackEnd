from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('create/user/', views.createUser),
    path('login/', views.loginUser),
    path('user/<int:id>/', views.getUserDetails),
    path('user/<int:id>/update/', views.updateUserDetails),
    path('logout/', views.logoutUser),
    path('delete/user/<int:id>/', views.deleteUser),
    path('userexists/<int:id>/', views.userExists),
    path('create/poll/', views.createPoll),
    path('delete/poll/<int:id>/', views.deletePoll),
    path('create/option/', views.createOption),
]