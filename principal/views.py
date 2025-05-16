from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

# Create your views here.

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        User = get_user_model()
        # Try to get full name, fallback to username
        name = getattr(user, 'get_full_name', lambda: None)() or user.username
        # Try to get role if it exists
        role = getattr(user, 'role', None)
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': name,
        }
        if role:
            data['role'] = role
        return Response(data)
