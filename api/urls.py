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

    path('delete/user/<int:id>/', views.deleteUser),
    path('delete/poll/<int:id>/', views.deletePoll),
    path('delete/friend/<int:id1>/<int:id2>/', views.unfriend),

    path('update/user/<int:id>/', views.updateUserDetails),

    path('user/<int:id>/', views.getUserDetails),
    path('userexists/<int:id>/', views.userExists),
    path('getfriends/<int:id>/', views.getFriends),
    path('searchusers/<str:query>/', views.searchUsers),

    path('friendrequest/<int:id1>/<int:id2>/', views.friendRequest),
    path('acceptfriendrequest/<int:id1>/<int:id2>/', views.acceptFriendRequest),
    path('rejectfriendrequest/<int:id1>/<int:id2>/', views.rejectFriendRequest),
    path('undofriendrequest/<int:id1>/<int:id2>/', views.undoFriendRequest),
    path('unfriend/<int:id1>/<int:id2>/', views.unfriend),
    path('block/<int:id1>/<int:id2>/', views.block),
    path('unblock/<int:id1>/<int:id2>/', views.unblock),

    path('polls/', views.getActivePolls),
    path('userpolls/<int:id>/', views.getPollByUser),

]
