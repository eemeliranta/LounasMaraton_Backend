from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.conf.urls import include

router = routers.DefaultRouter()
router.register(r'restaurant',      views.RestaurantViewSet, basename='restaurant')
# router.register(r'profile',         views.ProfileViewSet, basename='profile')
router.register(r'walk_history',    views.WalkHistoryViewSet, basename='walk_history')
# router.register(r'reward',          views.RewardViewSet, basename='reward')
router.register(r'claimed_reward',  views.ClaimedRewardViewSet, basename='claimed_reward')
router.register(r'user',            views.UserViewSet, basename='user')

urlpatterns = [
    path('', views.index, name='index'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    re_path('^api/', include(router.urls)),
]
