# users/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class ObtainAuthTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if not user:
            return Response({"detail": "Invalid credentials"}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
