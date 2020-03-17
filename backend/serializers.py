from rest_framework import serializers
from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward
from django.contrib.auth.models import User
from datetime import datetime


# Serializers
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
        user = self.context['request'].user

        if user.profile.walked_today():
            print(user, 'tried to walk a second time today.')
            return Walk_history.objects.filter(profile=user.profile).first()

        return Walk_history.objects.create(profile=user.profile,
                                           timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                                           **validated_data)


class RewardSerializer(serializers.HyperlinkedModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Restaurant.objects.all())

    class Meta:
        model = Reward
        fields = ['restaurant', 'description', 'cost']


class ClaimedRewardSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    reward = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Reward.objects.all())
    timestamp = serializers.DateTimeField(read_only=True)
    passcode = serializers.CharField(read_only=True)
    redeemed = serializers.BooleanField(read_only=False)

    class Meta:
        model = Claimed_reward
        fields = ['pk', 'profile', 'reward', 'timestamp', 'passcode', 'redeemed']

    def create(self, validated_data):
        user = self.context['request'].user

        user.profile.delete_unredeemed_rewards()

        # Check that user has enough credits to buy reward
        if user.profile.total_points < validated_data['reward'].cost:
            raise serializers.ValidationError({'Message': "Not enough credits"})

        return Claimed_reward.objects.create(profile=user.profile,
                                             timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                                             passcode=Claimed_reward.generate_passcode(),
                                             redeemed=False,
                                             **validated_data)

    def update(self, instance, validated_data):
        if self.context['request'].user.profile.manager_of != instance.reward.restaurant:
            raise serializers.ValidationError({'Message': "You are not a manager of this restaurant"})

        instance.redeemed = validated_data.get('redeemed', instance.redeemed)
        instance.save()
        return instance


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


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    reward_set = RewardSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'lunchtime_start', 'lunchtime_end', 'reward_set']
