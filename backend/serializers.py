# This file is used for the api
from rest_framework import serializers, viewsets
from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward
from django.contrib.auth.models import User, Group


# Serializers

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups',
                  'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined']


class WalkHistorySerializer(serializers.HyperlinkedModelSerializer):



    class Meta:
        model = Walk_history
        fields = ['id', 'profile', 'restaurant', 'distance', 'timestamp']


class RewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'restaurant', 'description', 'cost']


class ClaimedRewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Claimed_reward
        fields = ['id', 'reward', 'timestamp', 'passcode', 'redeemed']


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
        fields = ['id', 'phone', 'points_by_restaurant',
                  'walk_history_set', 'claimed_reward_set']


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    reward_set = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='reward-detail'
    )

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'lunchtime_start', 'lunchtime_end', 'manager',
                  'reward_set']
