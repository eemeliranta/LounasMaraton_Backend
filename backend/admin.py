from django.contrib import admin

from .models import Profile, Restaurant, Walk_history, Reward, Claimed_reward

class RewardsInline(admin.TabularInline):
    model = Reward
    extra = 0


class RestaurantAdmin(admin.ModelAdmin):
    fields = ['name','address','latitude','longitude','lunchtime_start','lunchtime_end','manager']
    inlines = [RewardsInline]
    list_display = ['name','address','manager','lunchtime_start','lunchtime_end']
    search_fields = ['name']

class ProfileAdmin(admin.ModelAdmin):
    fields = ['user','phone','points_by_restaurant_str']
    list_display = ['user','phone','total_points','total_points']
    readonly_fields = ['points_by_restaurant_str']
    search_fields = ['phone']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Walk_history)
admin.site.register(Claimed_reward)
