# This file is used for the api
from rest_framework import serializers, viewsets
from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward
from django.contrib.auth.models import User, Group


# Serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'groups', 'user_permissions',
                  'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


class WalkHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Walk_history
        fields = ['id', 'profile', 'restaurant', 'distance', 'date']


class RewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'restaurant', 'description', 'cost']


class ClaimedRewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Claimed_reward
        fields = ['id', 'reward', 'date', 'passcode', 'redeemed']



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    walk_history_set = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='walk_history-detail'
    )
    claimed_reward_set = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='claimed_reward-detail'
    )

    class Meta:
        model = Profile
        fields = ['id', 'phone', 'points_by_restaurant_str',
                  'walk_history_set', 'claimed_reward_set']


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'lunchtime_start', 'lunchtime_end', 'manager']
