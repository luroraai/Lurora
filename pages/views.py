from django.shortcuts import render
from .models import Pages, Contents
from wosvcore.breadcrumbs import Breadcrumb
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


def index_view(request):
    homepage_content = Contents.objects.filter(page__slug='homepage')
    main_pages = Pages.objects.filter(visible_home=True)
    context = {
        'homepage_content': homepage_content,
        'pages': main_pages,
    }
    return render(request, 'pages/main.html', context)


def page_detail(request, page_slug):
    page = Pages.objects.get(slug=page_slug)
    contents = Contents.objects.filter(page=page)
    context = {
        'page': page,
        'contents': contents,
    }
    context["breadcrumbs"] = [
        Breadcrumb(title=_("Homepage"), url=reverse("pages:index")),
        Breadcrumb(title=page.title, url=page.get_absolute_url())
    ]
    return render(request, 'pages/page_detail.html', context)
