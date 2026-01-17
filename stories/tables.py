#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 12.02.2025 23:08
#  Filename : tables.py
#  Last Modified : 12.02.2025 23:08
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
import django_tables2 as tables
from .models import Stories, Scenes
from django.urls import reverse
from django.utils.html import format_html


class StoriesTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = Stories
        fields = ('id', 'title', 'topic', 'scene_count', 'status', 'created_at', 'updated_at')
        template_name = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-bordered'}

    def render_actions(self, record):
        view_url = reverse('accounts:stories:detail', args=[record.pk])
        edit_url = reverse('accounts:stories:detail', args=[record.pk])
        delete_url = reverse('accounts:stories:detail', args=[record.pk])

        return format_html(
            '<div class="btn-group" role="group">'
            '<a href="{}" class="btn btn-info btn-sm" title="Görüntüle"><i class="fas fa-eye"></i></a>'
            '<a href="{}" class="btn btn-primary btn-sm" title="Düzenle"><i class="fas fa-edit"></i></a>'
            '<a href="{}" class="btn btn-danger btn-sm" title="Sil"><i class="fas fa-trash"></i></a>'
            '</div>',
            view_url, edit_url, delete_url
        )


class StoryBasicTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = Stories
        fields = ('title', 'topic', 'scene_count', 'status', 'created_at')
        template_name = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-bordered'}

    def render_actions(self, record):
        view_url = reverse('accounts:stories:detail', args=[record.pk])
        delete_url = reverse('accounts:stories:detail', args=[record.pk])

        return format_html(
            '<div class="btn-group" role="group">'
            '<a href="{}" class="btn btn-info btn-sm" title="View More"><i class="ki-outline ki-eye"></i></a>'
            '<a href="{}" class="btn btn-danger btn-sm" title="Delete"><i class="ki-outline ki-trash"></i></a>'
            '</div>',
            view_url, delete_url
        )
