# This file is used for the api
from rest_framework import serializers, viewsets
from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward
from django.contrib.auth.models import User, Group
from datetime import datetime


# Serializers

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class WalkHistorySerializer(serializers.HyperlinkedModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Restaurant.objects.all())
    distance = serializers.FloatField(min_value=0, max_value=None)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Walk_history
        fields = ['profile_id', 'restaurant', 'distance', 'timestamp']

    def create(self, validated_data):
        return Walk_history.objects.create(profile_id=self.context['request'].user.profile.id,
                                           timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                                           **validated_data)


class RewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reward
        fields = ['restaurant', 'description', 'cost']


class ClaimedRewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Claimed_reward
        fields = ['reward', 'timestamp', 'passcode', 'redeemed']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    # walk_history_set = WalkHistorySerializer(many=True, read_only=True)
    # claimed_reward_set = ClaimedRewardSerializer( many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['phone', 'points_by_restaurant']
        # 'walk_history_set', 'claimed_reward_set']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups', 'is_staff', 'is_active',
                  'is_superuser', 'last_login', 'date_joined', 'profile']


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    reward_set = RewardSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'lunchtime_start', 'lunchtime_end', 'manager',
                  'reward_set']
