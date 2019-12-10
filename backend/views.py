from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import redirect

from .models import User_type, User, Restaurant, Walk_history, Reward, Claimed_reward

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

