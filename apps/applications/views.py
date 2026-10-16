from django.shortcuts import render
from rest_framework import generics

from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated

class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
