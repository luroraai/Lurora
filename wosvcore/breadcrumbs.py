#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 10/29/24, 5:04 AM
#  Filename : breadcrumbs.py
#  Last Modified : 10/29/24, 5:04 AM
#  Project : wosvocorp
#  Module : wosvocorp
#
#  Copyright (c) 2024
# breadcrumbs.py
from django.urls import resolve, reverse
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Breadcrumb:
    title: str
    url: Optional[str] = None
    icon: Optional[str] = None


class BreadcrumbsManager:
    """
    Dinamik breadcrumbs yönetimi için ana sınıf
    """

    def __init__(self):
        self._registry = {}
        self._patterns = {}

    def register(self, url_name: str, title: str = None, parent: str = None, icon: str = None):
        """
        URL adına göre breadcrumb kaydı oluşturur
        """
        self._registry[url_name] = {
            'title': title,
            'parent': parent,
            'icon': icon
        }

    def register_pattern(self, url_pattern: str, callback):
        """
        Özel URL desenlerine göre başlık oluşturma fonksiyonu kaydeder
        """
        self._patterns[url_pattern] = callback

    def get_breadcrumbs(self, request) -> List[Breadcrumb]:
        """
        Request için breadcrumbs listesi oluşturur
        """
        current_url = resolve(request.path_info)
        breadcrumbs = []

        # Ana sayfa her zaman ilk sırada
        breadcrumbs.append(Breadcrumb(
            title=_("Home"),
            url=reverse('pages:index'),
            icon='home'
        ))

        # Mevcut URL için breadcrumb oluştur
        current_name = current_url.url_name
        if current_name:
            self._add_breadcrumb_chain(breadcrumbs, current_name, current_url)

        return breadcrumbs

    def _add_breadcrumb_chain(self, breadcrumbs: List[Breadcrumb], url_name: str, resolved_url):
        """
        URL hiyerarşisine göre breadcrumb zinciri oluşturur
        """
        if url_name not in self._registry:
            return

        # Önce parent breadcrumb'ları ekle
        parent = self._registry[url_name].get('parent')
        if parent:
            self._add_breadcrumb_chain(breadcrumbs, parent, resolved_url)

        # Başlığı belirle
        title = self._registry[url_name].get('title')
        if not title:
            # URL desenleri kontrol et
            for pattern, callback in self._patterns.items():
                if pattern in resolved_url.route:
                    title = callback(resolved_url)
                    break

            if not title:
                # Varsayılan başlık
                title = capfirst(url_name.replace('-', ' '))

        # URL oluştur
        try:
            url = reverse(url_name, args=resolved_url.args, kwargs=resolved_url.kwargs)
        except:
            url = None

        # Breadcrumb ekle
        breadcrumbs.append(Breadcrumb(
            title=title,
            url=url,
            icon=self._registry[url_name].get('icon')
        ))
