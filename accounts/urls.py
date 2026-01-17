#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 12.02.2025 20:01
#  Filename : urls.py
#  Last Modified : 12.02.2025 20:01
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
from django.urls import path, include
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    # path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('dashboard/', dashboard, name='dashboard'),
    path('stories/', include('stories.urls', namespace='stories')),
   
    path('profile/', profile, name='profile'),
    # path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', PasswordChangeView.as_view(), name='change_password'),
    # path('profile/delete/', delete_account, name='delete_account'),
    # path('profile/delete-confirm/', delete_account_confirm, name='delete_account_confirm'),
]
