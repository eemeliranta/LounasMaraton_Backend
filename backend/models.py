from django.db import models
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    lunchtime_start = models.TimeField()
    lunchtime_end = models.TimeField()
    menu_api = models.CharField(max_length=500)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager_of = models.ForeignKey(Restaurant, blank=True, null=True, on_delete=models.PROTECT)

    @property
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    # Total amount of points the user has
    @property
    def total_points(self):
        total_walked = Walk_history.objects.filter(profile=self).aggregate(Sum('distance')).get('distance__sum')
        claimed_rewards = Claimed_reward.objects.filter(profile=self, redeemed=True).aggregate(Sum('reward__cost')).get('reward__cost__sum')
        if total_walked and claimed_rewards:
            return total_walked - claimed_rewards
        elif total_walked:
            return total_walked
        return 0

    @property
    def total_walked(self):
        total_walked = Walk_history.objects.filter(profile=self).aggregate(Sum('distance')).get('distance__sum')
        if total_walked:
            return total_walked
        return 0

    @property
    def total_walked_month(self):
        start = (datetime.now() - timedelta(days=30))
        end = datetime.now()
        total_walked = Walk_history.objects.filter(profile=self, timestamp__range=(start, end)).aggregate(Sum('distance')).get('distance__sum')
        if total_walked:
            return total_walked
        return 0

    # List of points the user has, per restaurant
    # TODO, negate used points from restaurants
    # To be fixed if development continues
    def points_by_restaurant(self):
        return list(Walk_history.objects \
                    .filter(profile=self.pk) \
                    .values('restaurant') \
                    .annotate(Sum('distance')) \
                    .order_by('-distance__sum'))

    # List of points the user has, per restaurant, in string format
    def points_by_restaurant_str(self):
        points = self.points_by_restaurant()
        string = ""
        for i in points:
            rest = str(list(Restaurant.objects.filter(id=i.get('restaurant')))[0])
            string = '%s %s %s\n' % (string, rest, str(i.get('distance__sum')))
        return string

    # We check if user has already walked today
    def walked_today(self):
        records_today = Walk_history.objects.filter(profile=self,
                                                    timestamp__year=datetime.now().year,
                                                    timestamp__month=datetime.now().month,
                                                    timestamp__day=datetime.now().day
                                                    ).count()
        if records_today > 0:
            return True
        return False

    # Check if user has unredeemed rewards and deletes them
    def delete_unredeemed_rewards(self):
        rewards = Claimed_reward.objects.filter(profile=self, redeemed=False)
        for reward in rewards:
            reward.delete()

    class Meta:
        ordering = ['user']

    def __str__(self):
        return '%s (%s)' % (self.full_name, self.user.username)


# Automatically create a profile when user is created or modified
@receiver(post_save, sender=User)
def create_user_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
    else:
        instance.profile.save()


# TODO
# Need to save reward restaurant, description and cost to the claimed reward
# Else if restaurant changes the reward, already claimed rewards will also change
class Reward(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    description = models.CharField(max_length=64)
    cost = models.IntegerField(default=1)

    class Meta:
        ordering = ['restaurant', '-cost']

    def __str__(self):
        return '%s - %s (%s)' % (self.restaurant.name, self.description, self.cost)


class Claimed_reward(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    reward = models.ForeignKey(Reward, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(default=datetime.now)
    passcode = models.CharField(max_length=10)
    redeemed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    # Generates a 5 long string that is not being used in a reward that is unclaimed
    @staticmethod
    def generate_passcode():
        active_codes = list(Claimed_reward.objects.filter(redeemed=False).values('passcode'))
        while True:
            # 3 Length code = 42840 possible codes
            # 4 Length code = 1413720 possible codes
            new_code = uuid.uuid4().hex[:3].upper()
            if new_code not in active_codes:
                return new_code

    def __str__(self):
        return '%s %s Reward %s' % (self.profile, (self.redeemed and 'Redeemed' or 'Unredeemed'), self.reward)


class Walk_history(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    distance = models.FloatField(default=0)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    # Where the user started walking
    # This can be used in the future to show on a map where the customers come from
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return '%s %s Walked %skm' % (self.profile.user.first_name, self.profile.user.last_name, self.distance)
