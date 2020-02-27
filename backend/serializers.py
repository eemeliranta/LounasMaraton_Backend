# This file is used for the api
from rest_framework import serializers, viewsets
from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward
from django.contrib.auth.models import User, Group
from datetime import datetime


# Serializers

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['id', 'name']


class WalkHistorySerializer(serializers.HyperlinkedModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Restaurant.objects.all())
    distance = serializers.FloatField(min_value=0, max_value=None)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Walk_history
        fields = ['profile_id', 'restaurant', 'distance', 'timestamp']

    def create(self, validated_data):
        request = self.context['request']
        recordsToday = Walk_history.objects.filter(profile_id=request.user.profile.id,
                                                   timestamp__year=datetime.now().year,
                                                   timestamp__month=datetime.now().month,
                                                   timestamp__day=datetime.now().day
                                                   ).count()

        if recordsToday > 0:
            return Walk_history.objects.filter(profile_id=request.user.profile.id).first()

        return Walk_history.objects.create(profile_id=request.user.profile.id,
                                           timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                                           **validated_data)


class RewardSerializer(serializers.HyperlinkedModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Restaurant.objects.all())

    class Meta:
        model = Reward
        fields = ['restaurant', 'description', 'cost']


class ClaimedRewardSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Restaurant.objects.all())
    reward = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Reward.objects.all())

    class Meta:
        model = Claimed_reward
        fields = ['profile', 'reward', 'timestamp', 'passcode', 'redeemed']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    # walk_history_set = WalkHistorySerializer(many=True, read_only=True)
    # claimed_reward_set = ClaimedRewardSerializer( many=True, read_only=True)
    manager_of = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Restaurant.objects.all())

    class Meta:
        model = Profile
        fields = ['phone', 'manager_of', 'points_by_restaurant']
        # 'walk_history_set', 'claimed_reward_set']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']
        # , 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined'


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    reward_set = RewardSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'lunchtime_start', 'lunchtime_end', 'reward_set']
