from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import authenticate
from .utils import *


# Create your views here.
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
             username = serializer.validated_data.get('username')
             password = serializer.validated_data.get('password')
             
             user = authenticate(username=username, password=password)
             
             if user is not None:
                 token = get_tokens_for_user(user)
                 return Response(token, status=status.HTTP_200_OK)
             
             else:
                 return Response({"message": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            