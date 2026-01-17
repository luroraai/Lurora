from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_tables2.views import SingleTableView
from .tables import StoriesTable
from .forms import StoryForm, SceneKeyForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import google.generativeai as genai
from wosvcore.utils import DallEGenerator, StoryGenerator
import requests
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import base64
import uuid
import re


class StoryListView(LoginRequiredMixin, SingleTableView):
    table_class = StoriesTable
    queryset = Stories.objects.all()
    template_name = 'accounts/story_list.html'
    context_object_name = 'stories'

    def get_queryset(self):
        return Stories.objects.filter(author=self.request.user)


class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Stories
    # fields = ['title', 'topic', 'scene_count']
    template_name = 'accounts/story_form.html'
    success_url = '/stories/'
    form_class = StoryForm

    def get_queryset(self):
        return Stories.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'in_progress'
        story = form.save()
        service = StoryGenerator()
        generated_content = service.generate_story(topic=story.topic, scene_count=story.scene_count)
        if generated_content:
            story.content = generated_content
            story.status = 'completed'
            story.save()
            messages.success(self.request, 'Story content has been generated successfully.')
        else:
            messages.error(self.request, 'Story content generation failed.')
        return redirect('accounts:stories:detail', pk=story.pk)


class StoryDetailView(LoginRequiredMixin, DetailView):
    model = Stories
    template_name = 'accounts/story_detail.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Scenes.objects.filter(story=self.object).delete()
        context['scenes'] = Scenes.objects.filter(story=self.object)
        context['scene_key_form'] = SceneKeyForm
        context['has_content'] = bool(self.object.content)
        context['has_scenes'] = self.object.has_scenes()

        return context


def create_scenes(request, story_id):
    if request.method == 'POST':
        story = Stories.objects.get(id=story_id)
        # Implement your logic to create scenes from story.content
        # This is just a placeholder implementation
        service = StoryGenerator()
        scene_generator = service.generate_scenes(story)
        # Sahne sayısını kontrol et
        actual_scene_count = Scenes.objects.filter(story=story).count()
        if actual_scene_count != story.scene_count:
            print(f"Uyarı: Beklenen sahne sayısı {story.scene_count:}, oluşturulan sahne sayısı {actual_scene_count}")

    return redirect('accounts:stories:detail', pk=story_id)


def generate_story(request, story_id):
    if request.method == 'POST':
        try:
            story = get_object_or_404(Stories, pk=story_id)
            service = StoryGenerator()
            generated_content = service.generate_story(topic=story.topic, scene_count=story.scene_count)

            if generated_content:
                story.content = generated_content
                story.status = 'completed'
                story.save()
                messages.success(request, 'Story content has been generated successfully.')
            else:
                messages.error(request, 'Story content generation failed.')

        except Exception as e:
            messages.error(request, f'Error generating story: {str(e)}')
    return redirect('accounts:stories:detail', pk=story_id)


@login_required
def scene_key_update(request, pk):
    scene = get_object_or_404(Scenes, pk=pk)
    form = SceneKeyForm(request.POST or None, instance=scene)
    if form.is_valid():
        form.save()
        messages.success(request, f'{scene.scene_title} Sahne Kaydedildi!')
        return redirect('accounts:stories:detail', pk=scene.story.pk)
    else:
        messages.error(request, 'Scene key update failed!')
        return redirect('accounts:stories:detail', pk=scene.story.pk)


class CreateImageView(LoginRequiredMixin, DetailView):
    model = Scenes
    template_name = 'stories/scene_detail.html'
    context_object_name = 'scene'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scene'] = self.get_object()
        image_url = DallEGenerator().generate_image(context['scene'].content)
        print(image_url)
        if image_url:
            scene = Scenes.objects.get(id=context['scene'].id)
            scene.image_url = image_url

            response = requests.get(image_url)
            if response.status_code == 200:
                file_name = f"scene_{scene.id}.jpg"
                file_path = os.path.join(settings.MEDIA_ROOT, 'scenes', file_name)
                default_storage.save(file_path, ContentFile(response.content))
                scene.generated_image.name = f"scenes/{file_name}"

            scene.save()
            messages.success(self.request, 'Image generated successfully!')
        else:
            messages.error(self.request, 'Failed to generate image. Please try again.')
        return context

    def get_queryset(self):
        return Scenes.objects.filter(story__author=self.request.user)


@csrf_exempt
@login_required()
def generate_image(request, scene_id):
    try:
        scene = get_object_or_404(Scenes, id=scene_id)
        image_url = DallEGenerator().generate_image(scene.content)
        print(image_url)
        if image_url:
            scene.image_url = image_url

            response = requests.get(image_url)
            if response.status_code == 200:
                file_name = f"scene_{scene.id}.jpg"
                safe_file_name = os.path.basename(file_name)
                # file_path = os.path.join(settings.MEDIA_ROOT, 'scenes', file_name)
                file_path = default_storage.save(f"scenes/{safe_file_name}", ContentFile(response.content))
                default_storage.save(file_path, ContentFile(response.content))
                scene.generated_image.name = f"scenes/{file_name}"
            scene.save()
            return JsonResponse({
                'success': True,
                'message': 'Image generated successfully!',
                'image_url': scene.generated_image.url  # URL'yi generated_image'dan al
            })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
@login_required
def save_watermarked_image(request, scene_id):
    if request.method == 'POST':
        try:
            scene = get_object_or_404(Scenes, id=scene_id, story__author=request.user)

            # Get the image data from the request
            image_data = request.POST.get('image_data', '')
            code = request.POST.get('code', '')

            if not image_data:
                return JsonResponse({'success': False, 'error': 'No image data provided'}, status=400)

            # Remove the data:image/png;base64, prefix
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]

            # Convert base64 to binary
            image_binary = base64.b64decode(image_data)

            # Generate a unique filename
            filename = f"watermarked_scene_{scene_id}_{uuid.uuid4().hex[:8]}.png"

            # Save the image to the scene_image field
            scene.keyword = code
            scene.scene_image.save(filename, ContentFile(image_binary), save=True)

            return JsonResponse({
                'success': True,
                'message': 'Image saved successfully!',
                'image_url': scene.scene_image.url
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def delete_scene(request, pk):
    if request.method == 'POST':
        try:
            scene = get_object_or_404(Scenes, id=pk, story__author=request.user)
            scene.delete()
            return JsonResponse({'success': True, 'message': 'Scene deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
