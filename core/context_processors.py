#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 25.03.2025 01:16
#  Filename : context_processors.py
#  Last Modified : 25.03.2025 01:16
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
from django.conf import settings
from pages.models import Pages
from wosvcore.breadcrumbs import BreadcrumbsManager

breadcrumbs = BreadcrumbsManager()


def site_processor(request):
    """
    A context processor that adds site-specific data to the request context.
    """
    site_name = "Lurora"
    site_url = "https://lurora.com"
    site_description = ""
    breadcrumbs.get_breadcrumbs(request)
    header_menu = Pages.objects.filter(visible_header=True)
    footer_menu = Pages.objects.filter(visible_footer=True)
    context = {
        'site_name': site_name,
        'site_url': site_url,
        'site_description': site_description,
        'breadcrumbs': breadcrumbs,
        'header_menu': header_menu,
        'footer_menu': footer_menu
    }

    return context


def breadcrumbs_processor(request):
    """
    Template'lere breadcrumbs ekleyen context processor
    """
    return {
        'breadcrumbs': breadcrumbs.get_breadcrumbs(request)
    }
