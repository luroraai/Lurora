#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 6.03.2025 20:20
#  Filename : absmodel.py
#  Last Modified : 6.03.2025 20:20
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from unidecode import unidecode
from tinymce.models import HTMLField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill, SmartResize
from wosvcore.abschoices import StatusChoices
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill, SmartResize
from wosvcore.utils import validate_file_extension, generate_unique_filename
from functools import partial


class DatedBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        abstract = True


class StatusBaseModel(models.Model):
    """
        An abstract base model that provides a 'status' field.
        """
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.ACTIVE,
                              verbose_name=_('Status'))

    class Meta:
        abstract = True


class UserTrackingBaseModel(models.Model):
    """
    An abstract base model that provides 'created_by' and 'updated_by' fields.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_created',
        verbose_name=_('Created by')
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_updated',
        verbose_name=_('Updated by')
    )

    class Meta:
        abstract = True


class AbstractCoreModel(DatedBaseModel):
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        abstract = True


class AbstractWithStatusModel(AbstractCoreModel, StatusBaseModel):
    class Meta:
        abstract = True


class AbstractPublicModel(AbstractCoreModel, StatusBaseModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    subtitle = models.CharField(max_length=255, blank=True, verbose_name=_('Subtitle'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        abstract = True


class AbstractContentModel(AbstractPublicModel):
    content = HTMLField(verbose_name=_('Content'), blank=True)

    class Meta:
        abstract = True
