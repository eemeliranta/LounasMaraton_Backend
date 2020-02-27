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
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user.pk)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer

    # Vain admin voi tehdä ravintolan
    # Managerit voivat muokata omaa ravintolaa

    # def list(self, request):
    #     queryset = Restaurant.objects.all()
    #     serializer = serializers.RestaurantSerializer(queryset, many=True, context={'request':request})
    #     return Response(serializer.data)

    def create(self, request):
        pass

    # def retrieve(self, request, pk=None):
    #     pass
    #
    # def update(self, request, pk=None):
    #     pass
    #
    # def partial_update(self, request, pk=None):
    #     pass
    #
    def destroy(self, request, pk=None):
        pass


class WalkHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.WalkHistorySerializer

    # Custom queryset to return only allowed results
    def get_queryset(self):
        # if self.request.user.is_staff:
        #     return Walk_history.objects.all()
        # else:
        return Walk_history.objects.filter(profile_id=self.request.user.pk)


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = serializers.RewardSerializer


class ClaimedRewardViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ClaimedRewardSerializer

    def get_queryset(self):
        return Claimed_reward.objects.filter(profile__user=self.request.user.pk)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


# class GroupViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Group.objects.all()
#     serializer_class = serializers.GroupSerializer
