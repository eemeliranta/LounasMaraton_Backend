from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from rest_framework import viewsets, status, permissions, generics, mixins
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward
from django.contrib.auth.models import User, Group
from . import serializers


def index(request):
    return HttpResponse("Lounas Maraton")


# ViewSets for the API
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user.pk)


class RestaurantViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class WalkHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.WalkHistorySerializer

    # Return only users own results
    def get_queryset(self):
        return Walk_history.objects.filter(profile_id=self.request.user.pk)


# class RewardViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.AllowAny,)
#     queryset = Reward.objects.all()
#     serializer_class = serializers.RewardSerializer


class ClaimedRewardViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ClaimedRewardSerializer

    def get_queryset(self):
        return Claimed_reward.objects.filter(profile__user=self.request.user.pk)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer
    queryset = User.objects.all()


class RewardClaimingAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.RewardClaimingSerializer
    queryset = Claimed_reward.objects.all()
