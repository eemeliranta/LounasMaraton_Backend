from django.urls import path, include, re_path
from rest_framework import routers
from . import views, serializers

router = routers.DefaultRouter()
router.register(r'restaurant',      serializers.RestaurantViewSet)
router.register(r'user',            serializers.UserViewSet)
router.register(r'user_type',       serializers.UserTypeViewSet)
router.register(r'walk_history',    serializers.WalkHistoryViewSet)
router.register(r'reward',          serializers.RewardViewSet)
router.register(r'claimed_reward',  serializers.ClaimedRewardViewSet)

urlpatterns = [
    path('', views.index, name='index'),

    re_path('^api/', include(router.urls)),
]