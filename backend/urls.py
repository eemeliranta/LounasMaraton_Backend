from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register(r'restaurant',      views.RestaurantViewSet)
router.register(r'profile',         views.ProfileViewSet)
router.register(r'walk_history',    views.WalkHistoryViewSet)
router.register(r'reward',          views.RewardViewSet)
router.register(r'claimed_reward',  views.ClaimedRewardViewSet)
router.register(r'user',            views.UserViewSet)
router.register(r'group',            views.GroupViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    re_path('^api/', include(router.urls)),
]