from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import *
from .serializers import *

@api_view(['GET'])
def getData(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    print("here")
    if serializer.is_valid():
        print("Worked")
        serializer.save()
    return Response(serializer.data)