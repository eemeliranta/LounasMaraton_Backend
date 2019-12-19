from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User_type, Profile, Restaurant, Walk_history, Reward, Claimed_reward
from . import serializers


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# ViewSets for the API
class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = User_type.objects.all()
    serializer_class = serializers.UserTypeSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class WalkHistoryViewSet(viewsets.ModelViewSet):
    queryset = Walk_history.objects.all()
    serializer_class = serializers.WalkHistorySerializer


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = serializers.RewardSerializer


class ClaimedRewardViewSet(viewsets.ModelViewSet):
    queryset = Claimed_reward.objects.all()
    serializer_class = serializers.ClaimedRewardSerializer
