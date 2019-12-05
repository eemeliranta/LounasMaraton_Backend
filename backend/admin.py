from django.contrib import admin

from .models import User_type, User, Restaurant, Walk_history, Reward, Claimed_reward

class RewardsInline(admin.TabularInline):
    model = Reward
    extra = 0


class RestaurantAdmin(admin.ModelAdmin):
    fields = ('name','address','latitude','longitude','lunchtime_start','lunchtime_end','manager')
    inlines = [RewardsInline]
    list_display = ('name','address','manager','lunchtime_start','lunchtime_end')
    search_fields = ['name']

class UserAdmin(admin.ModelAdmin):
    fields = ('first_name','last_name','email','phone','user_type','points_by_restaurant_str')
    list_display = ('first_name','last_name','email','phone','user_type','total_points','total_points')
    readonly_fields = ['points_by_restaurant_str']
    search_fields = ['first_name','last_name','email','phone','user_type']


admin.site.register(User_type)
admin.site.register(User, UserAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Walk_history)
admin.site.register(Claimed_reward)
