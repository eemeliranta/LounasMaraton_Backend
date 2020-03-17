from django.contrib import admin

from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward


class RewardsInline(admin.TabularInline):
    model = Reward
    extra = 0

class ClaimedRewardsInline(admin.TabularInline):
    model = Claimed_reward
    extra = 0
    readonly_fields = ['reward','passcode']


class WalkHistoryInline(admin.TabularInline):
    model = Walk_history
    extra = 0


class RestaurantAdmin(admin.ModelAdmin):
    fields = ['name', 'address', 'latitude', 'longitude', 'lunchtime_start', 'lunchtime_end']
    inlines = [RewardsInline]
    list_display = ['name', 'address', 'lunchtime_start', 'lunchtime_end']
    search_fields = ['name']


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'total_points', 'manager_of']
    list_display = ['user', 'total_points', 'manager_of']
    readonly_fields = ['user','total_points']
    inlines = [ClaimedRewardsInline, WalkHistoryInline]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
