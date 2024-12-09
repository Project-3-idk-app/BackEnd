from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import logout
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

@api_view(['POST'])
def createVote(request):
    serializer = VoteSerializer(data=request.data)
    poll_id = request.data.get('poll')
    user_id = request.data.get('user')
    
    try:
        poll = Poll.objects.get(poll_id=poll_id)
        if poll.user.id == user_id:
            return Response({"error": "Poll creator cannot vote on their own poll"}, status=status.HTTP_400_BAD_REQUEST)
    except Poll.DoesNotExist:
        return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if Vote.objects.filter(poll_id=poll_id, user_id=user_id).exists():
        return Response({"error": "User has already voted on this poll"}, status=status.HTTP_400_BAD_REQUEST)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def friendRequest(request, id1, id2):
    # id1 is the user sending the request
    try:
        Friend.objects.get(user_id1=id2, user_id2=id1)
        return Response({"error": "Friendship already exists"}, status=status.HTTP_400_BAD_REQUEST)
    except Friend.DoesNotExist:
        request = FriendSerializer(data={"user_id1": id2, "user_id2": id1, "status": 0})
        # id2, id1 is the user receiving the request
        pending = FriendSerializer(data={"user_id1": id1, "user_id2": id2, "status": 1})
        # id1, id2 is the user sending the request
        if request.is_valid() and pending.is_valid():
            request.save()
            pending.save()
            return Response(request.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def acceptFriendRequest(request, id1, id2):
    try:
        friend = Friend.objects.get(user_id1=id1, user_id2=id2)
        friend1 = Friend.objects.get(user_id1=id2, user_id2=id1)
        friend.status = 2
        friend1.status = 2
        friend.save()
        friend1.save()
        return Response({"message": "Friendship accepted"}, status=status.HTTP_200_OK)
    except Friend.DoesNotExist:
        return Response({"error": "Friendship not found"}, status=status.HTTP_404_NOT_FOUND)

def delete_friendship(id1, id2):
    """
    Helper function to delete a friendship between two users.
    Returns a tuple: (success, message or error)
    """
    try:
        Friend.objects.filter(user_id1=id1, user_id2=id2).delete()
        Friend.objects.filter(user_id1=id2, user_id2=id1).delete()
        return True, "Friendship successfully deleted"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

@api_view(['DELETE'])
def rejectFriendRequest(request, id1, id2):
    success, message = delete_friendship(id1, id2)
    if success:
        return Response({"message": "Friendship request rejected"}, status=status.HTTP_200_OK)
    return Response({"error": message}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def undoFriendRequest(request, id1, id2):
    success, message = delete_friendship(id1, id2)
    if success:
        return Response({"message": "Friendship request undone"}, status=status.HTTP_200_OK)
    return Response({"error": message}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def unfriend(request, id1, id2):
    success, message = delete_friendship(id1, id2)
    if success:
        return Response({"message": "Friendship removed"}, status=status.HTTP_200_OK)
    return Response({"error": message}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def block(request, id1, id2):
    try:
        friend = Friend.objects.get(user_id1=id1, user_id2=id2)
        friend1 = Friend.objects.get(user_id1=id2, user_id2=id1)
        friend.status = 3
        friend.save()
        friend1.delete()
        return Response({"message": "Person blocked"}, status=status.HTTP_200_OK)
    except Friend.DoesNotExist:
        try:
            friend = Friend(user_id1=id1, user_id2=id2, status=3)
            friend.save()
            return Response({"message": "Person blocked"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Failed to create friendship records", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
@api_view(['DELETE'])
def unblock(request, id1, id2):
    friend = Friend.objects.filter(user_id1=id1, user_id2=id2, status=3)
    friend.delete()
    return Response({"message": "Person unblocked"}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def getFriends(request, id):
    friends = Friend.objects.filter(user_id1=id, status=2)
    serializer = FriendSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getNotifications(request, id):
    friends = Friend.objects.filter(user_id1=id, status__in=[0, 1])
    serializer = FriendSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def searchUsers(request, query):
    users = User.objects.filter(username__icontains=query)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getActivePolls(request):
    expired_polls = Poll.objects.filter(is_active=True, created_on__lt=datetime.now() - timedelta(days=1))
    expired_polls.update(is_active=False)
    
    polls = Poll.objects.filter(is_active=True)
    serializer = PollSerializer(polls, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getActivePollsByUser(request, id):
    expired_polls = Poll.objects.filter(is_active=True, created_on__lt=datetime.now() - timedelta(days=1))
    expired_polls.update(is_active=False)

    try:
        user = User.objects.get(id=id)
        polls = Poll.objects.filter(is_active=True).exclude(vote__user_id=id).exclude(user_id=id)
        poll_data = []

        for poll in polls:
            options = Option.objects.filter(poll=poll)
            option_data = []
            for option in options:
                votes = Vote.objects.filter(option=option).count()
                option_data.append({
                    "option_id": option.option_id,
                    "poll": option.poll.poll_id,
                    "user": option.user.id,
                    "option_text": option.option_text,
                    "votes": votes
                })
            poll_data.append({
                "poll_id": poll.poll_id,
                "user": poll.user.id,
                "title": poll.title,
                "is_active": poll.is_active,
                "is_public": poll.is_public,
                "created_on": poll.created_on,
                "expires_on": poll.expires_on,
                "pollVotes" : Vote.objects.filter(poll=poll).count(),
                "options": option_data
            })

        data = {
            "userId": user.id,
            "polls": poll_data
        }
        return Response(data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getPollByUser(request, id):
    expired_polls = Poll.objects.filter(is_active=True, created_on__lt=datetime.now() - timedelta(days=1))
    expired_polls.update(is_active=False)

    try:
        user = User.objects.get(id=id)
        polls = Poll.objects.filter(user=user)
        poll_data_active = []
        poll_data_inactive = []

        for poll in polls:
            options = Option.objects.filter(poll=poll)
            option_data = []
            for option in options:
                votes = Vote.objects.filter(option=option).count()
                option_data.append({
                    "option": option.option_text,
                    "votes": votes
                })
            if poll.is_active:
                poll_data_active.append({
                    "pollId": poll.poll_id,
                    "pollTitle": poll.title,
                    "pollVotes" : Vote.objects.filter(poll=poll).count(),
                    "options": option_data
                })
            else:
                poll_data_inactive.append({
                    "pollId": poll.poll_id,
                    "pollTitle": poll.title,
                    "pollVotes" : Vote.objects.filter(poll=poll).count(),
                    "options": option_data
                })

        data = {
            "userId": user.id,
            "polls_active": poll_data_active,
            "polls_inactive": poll_data_inactive
        }
        return Response(data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)