from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('login/', views.loginUser),
    path('logout/', views.logoutUser),

    path('create/user/', views.createUser),
    path('create/poll/', views.createPoll),
    path('create/option/', views.createOption),
    path('create/vote/', views.createVote),
    path('create/friend/', views.createFriend),

    path('delete/user/<int:id>/', views.deleteUser),
    path('delete/poll/<int:id>/', views.deletePoll),
    path('delete/friend/<int:id1>/<int:id2>/', views.deleteFriend),

    path('update/friend/<int:id1>/<int:id2>/<int:status>/', views.updateFriend),
    path('update/user/<int:id>/', views.updateUserDetails),

    path('user/<int:id>/', views.getUserDetails),
    path('userexists/<int:id>/', views.userExists),
    path('getfriends/<int:id>/', views.getFriends),
    path('searchusers/<str:search>/', views.searchUsers),

]