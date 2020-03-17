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
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Restaurant.objects.all())
    distance = serializers.FloatField(min_value=0, max_value=None)
    timestamp = serializers.DateTimeField(read_only=True)
    latitude = serializers.FloatField(read_only=False)
    longitude = serializers.FloatField(read_only=False)

    class Meta:
        model = Walk_history
        fields = ['profile', 'restaurant', 'distance', 'timestamp', 'latitude', 'longitude']

    def create(self, validated_data):
        request = self.context['request']

        if request.user.profile.walked_today():
            print(request.user, 'tried to walk a second time today.')
            return Walk_history.objects.filter(profile=request.user.profile).first()

        return Walk_history.objects.create(profile=request.user.profile,
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
        fields = ['profile', 'reward', 'timestamp', 'passcode', 'redeemed', 'generate_passcode']

    def create(self, validated_data):
        request = self.context['request']

        if request.user.profile.walked_today():
            print(request.user, 'tried to walk a second time today.')
            return Walk_history.objects.filter(profile=request.user.profile).first()

        return Walk_history.objects.create(profile=request.user.profile,
                                           timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                                           **validated_data)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    manager_of = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Restaurant.objects.all())

    class Meta:
        model = Profile
        fields = ['manager_of', 'total_points']


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
