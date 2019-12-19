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
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class WalkHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WalkHistorySerializer

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
    queryset = Claimed_reward.objects.all()
    serializer_class = serializers.ClaimedRewardSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
