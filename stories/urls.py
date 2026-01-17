#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 13.02.2025 00:55
#  Filename : urls.py
#  Last Modified : 13.02.2025 00:55
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025

from django.urls import path, include
from .views import *

app_name = 'stories'

urlpatterns = [
    path('', StoryListView.as_view(), name='index'),
    path('create/', StoryCreateView.as_view(), name='create'),
    path('<int:pk>/', StoryDetailView.as_view(), name='detail'),
    path('create_image/<int:pk>/', CreateImageView.as_view(), name='create_image'),
    path('scene_update_key/<int:pk>/', scene_key_update, name='scene_update_key'),
    path('scene/<int:scene_id>/generate-image', generate_image, name='generate_image'),
    path('scene/<int:scene_id>/save-watermarked/', save_watermarked_image, name='save_watermarked_image'),
    path('generate_story/<int:story_id>/', generate_story, name='generate_story'),
    path('create_scenes/<int:story_id>/', create_scenes, name='create_scenes')
    # path('update/<int:pk>', StoryUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>', StoryDeleteView.as_view(), name='delete'),
    # path('detail/<int:pk>', StoryDetailView.as_view(), name='detail'),
    # path('scene/create/<int:pk>', SceneCreateView.as_view(), name='scene_create'),
    # path('scene/update/<int:pk>', SceneUpdateView.as_view(), name='scene_update'),
    # path('scene/delete/<int:pk>', SceneDeleteView.as_view(), name='scene_delete'),
]
