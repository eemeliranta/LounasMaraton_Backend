from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward
from django.contrib.auth.models import User, Group
from . import serializers


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


def index(request):
    return HttpResponse("Lounasmaraton backend")


# ViewSets for the API
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Profile.objects.none()
        elif self.request.user.is_staff:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=self.request.user.pk)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class WalkHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WalkHistorySerializer

    # Custom queryset to return only allowed results
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Walk_history.objects.none()
        elif self.request.user.is_staff:
            return Walk_history.objects.all()
        else:
            return Walk_history.objects.filter(pk=self.request.user.pk)


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = serializers.RewardSerializer


class ClaimedRewardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClaimedRewardSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Claimed_reward.objects.none()
        elif self.request.user.is_staff:
            return Claimed_reward.objects.all()
        else:
            return Claimed_reward.objects.filter(profile__user=self.request.user.pk)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        elif self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.pk)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
