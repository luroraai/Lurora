#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 13.02.2025 23:56
#  Filename : urls.py
#  Last Modified : 13.02.2025 23:56
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
from django.urls import path, include
from .views import *

app_name = 'pages'

urlpatterns = [
    path('', index_view, name='index'),
    path("home/", index_view, name="home"),
    path("<slug:page_slug>/", page_detail, name="detail"),
]
