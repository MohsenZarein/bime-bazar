from rest_framework.views import APIView
from rest_framework import generics
from .serializers import CreateUserSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class CreateUserAPI(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):

        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserAPI(generics.RetrieveAPIView):
  permission_classes = [permissions.IsAuthenticated,]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user
  
  def get_serializer(self, *args, **kwargs):
    return super(UserAPI, self).get_serializer(*args, **kwargs)
