from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from base.models import *
from .serializers import *
from rest_framework import status
from datetime import date, timedelta, datetime

@api_view(['GET'])
def getData(request):
    users = User.objects.all()
    polls = Poll.objects.all()
    options = Option.objects.all()
    votes = Vote.objects.all()
    friends = Friend.objects.all()
    userSerializer = UserSerializer(users, many=True)
    pollSerializer = PollSerializer(polls, many=True)
    optionSerializer = OptionSerializer(options, many=True)
    voteSerializer = VoteSerializer(votes, many=True)
    friendSerializer = FriendSerializer(friends, many=True)
    data = {
        "users": userSerializer.data,
        "polls": pollSerializer.data,
        "options": optionSerializer.data,
        "votes": voteSerializer.data,
        "friends": friendSerializer.data
    }
    return Response(data)

@api_view(['POST'])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginUser(request):
    """Login a user via OAuth ID."""
    oauth_id = request.data.get('id')  # The OAuth ID sent by the client
    
    try:
        user = User.objects.get(id=oauth_id)  # Assuming `id` is the OAuth ID
        request.session['user_id'] = user.id
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getUserDetails(request, id):
    """Get details of a specific user."""
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def updateUserDetails(request, id):
    """Update details of a specific user."""
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def logoutUser(request):
    """Logout the user."""
    logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteUser(request, id):
    """Delete a user."""
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response({"message": "User deleted"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def userExists(request, id):
    """Check if a user exists."""
    try:
        User.objects.get(id=id)
        return Response({"exists": True})
    except User.DoesNotExist:
        return Response({"exists": False})
    
@api_view(['POST'])
def createPoll(request):
    # Create the poll with the user
    data = request.data.copy()
    data['is_active'] = True
    data['is_public'] = True
    data['created_on'] = date.today() # Set the created_on date to today
    data['expires_on'] = datetime.today() + timedelta(days=1)

    serializer = PollSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deletePoll(request, id):
    try:
        poll = Poll.objects.get(poll_id=id)
        poll.delete()
        return Response({"message": "Poll deleted"}, status=status.HTTP_200_OK)
    except Poll.DoesNotExist:
        return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def createOption(request):
    serializer = OptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)