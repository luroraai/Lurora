from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from .models import Stories, Scenes


class ScenesInline(StackedInline):
    model = Scenes
    extra = 0
    fields = ('scene_title', 'content', 'gen_content', 'scene_number', 'keyword', 'image_url', 'created_at')
    readonly_fields = ('scene_title', 'content', 'gen_content', 'scene_number', 'keyword', 'image_url', 'created_at')


@admin.register(Stories)
class StoriesAdmin(ModelAdmin):
    inlines = [ScenesInline]
    list_display = ('title', 'author', 'created_at')
    fields = ('title', 'author', 'content',)
