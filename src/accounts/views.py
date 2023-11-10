from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.utils import get_tokens_for_user

from .serializer import AuthenticationSerializer


class SignupView(APIView):
    """
    A Logic for user Sign-up.
    """

    permission_classes = (AllowAny,)
    serializer_class = AuthenticationSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("password")

            try:
                user = get_user_model().objects.get(username=username)

            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(
                    username=username,
                    password=password,
                )

            content = {"detail": "Signup successful."}

            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("password")

            user = authenticate(username=username, password=password)
            if not user:
                content = {"detail": "Invalid credentials."}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

            tokens = get_tokens_for_user(user)

            content = {"detail": "User verified, login successful."}

            content.update(tokens)
            return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
