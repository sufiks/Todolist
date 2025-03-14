from core.models import User
from core.serializers import (CreateUserSerializer, LoginSerializer,
                              ProfileSerializer, UpdatePasswordSerializer)
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response


class SignupView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated] # Аутентификация
    def get_object(self) -> User: # Возвращает пользователя, потому что в queryset лежит user
        return self.request.user
    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdatePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user

