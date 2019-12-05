from django.db import models
from datetime import datetime
from django.db.models import Sum

class User_type(models.Model):
    type = models.CharField(max_length=64)

    class Meta:
        ordering = ['type']

    def __str__(self):
        return self.type

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_type = models.ForeignKey(User_type, on_delete=models.PROTECT)
    email = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=200)

    def total_points(self):
        return str(Walk_history.objects.filter(user=self.pk).aggregate(Sum('distance')).get('distance__sum'))

    def points_by_restaurant(self):
        return list(Walk_history.objects\
            .filter(user=self.pk)\
            .values('restaurant')\
            .annotate(Sum('distance'))\
            .order_by('-distance__sum'))

    def points_by_restaurant_str(self):
        points = self.points_by_restaurant()
        string = ""
        for i in points:
            rest = str(list(Restaurant.objects.filter(id=i.get('restaurant')))[0])
            string = '%s %s %s\n' % (string, rest, str(i.get('distance__sum')))
        return string

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    lunchtime_start = models.TimeField()
    lunchtime_end = models.TimeField()
    menu_api = models.CharField(max_length=500)
    manager = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Reward(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    description = models.CharField(max_length=64)
    cost = models.IntegerField(default=1)

    class Meta:
        ordering = ['restaurant','-cost']

    def __str__(self):
        return '%s - %s (%s)' % (self.restaurant.name, self.description, self.cost)


class Claimed_reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reward = models.ForeignKey(Reward, on_delete=models.PROTECT)
    date = models.DateTimeField(default=datetime.now)
    passcode = models.CharField(max_length=200)
    redeemed = models.BooleanField(default=False)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return '%s %s Claimed %s' % (self.user.first_name, self.user.last_name, self.passcode)


class Walk_history(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    distance = models.FloatField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ['restaurant']

    def __str__(self):
        return '%s %s Walked %skm' % (self.user.first_name, self.user.last_name, self.distance)