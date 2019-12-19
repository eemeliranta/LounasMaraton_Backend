# This file is used for the api
from rest_framework import serializers, viewsets
from .models import User_type, Profile, Restaurant, Walk_history, Reward, Claimed_reward


# Serializers

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


class UserTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User_type
        fields = ['id', 'type']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_type = serializers.StringRelatedField()
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
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'user_type', 'points_by_restaurant_str',
                  'walk_history_set', 'claimed_reward_set']


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'lunchtime_start', 'lunchtime_end', 'manager']


