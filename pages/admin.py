from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from tinymce.widgets import TinyMCE
from .models import Pages, Contents
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from tinymce.models import HTMLField


class ContentsInline(StackedInline):
    model = Contents
    extra = 0
    fields = ["content_type", "title", "subtitle", "content", "status"]
    formfield_overrides = {
        HTMLField: {"widget": TinyMCE()},
    }


@admin.register(Pages)
class PagesAdmin(DraggableMPTTAdmin, ModelAdmin):
    inlines = [ContentsInline]
    mptt_indent_field = "title"
    list_display_links = ("title",)
    list_display = ["tree_actions",
                    "title",
                    "slug",
                    "page_type",
                    "sort_order",
                    "visible_footer",
                    "visible_header",
                    "visible_home",
                    "created_at",
                    "status", ]
    list_filter = ["status", "created_at", "updated_at"]
    fields = ("title", "subtitle", "description", "slug", "parent", "page_type", "sort_order", "visible_footer", "visible_header", "visible_home", "content", "status")
    formfield_overrides = {
        HTMLField: {"widget": TinyMCE()},
    }
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Contents)
class ContentsAdmin(DraggableMPTTAdmin, ModelAdmin):
    form = MPTTAdminForm
    mptt_indent_field = "title"
    list_display_links = ("title",)
    list_display = ["tree_actions",
                    "title",
                    "content_type",
                    "parent",
                    "page", "created_at", "updated_at", 'visible_home']
    list_filter = ["content_type", "parent", "created_at", "updated_at"]
