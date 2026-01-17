from django.db import models
from wosvcore.absmodel import AbstractPublicModel, AbstractCoreModel, AbstractContentModel
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill, SmartResize
from wosvcore.utils import validate_file_extension, generate_unique_filename
from functools import partial


class StoryCategories(AbstractPublicModel, MPTTModel):
    image = ProcessedImageField(
        verbose_name="Page Image",
        upload_to=partial(generate_unique_filename, field_name='title', upload_to='story_categories'),
        processors=[ResizeToFit(1024, 1024)],
        options={"quality": 90},
        validators=[validate_file_extension],
        format="WEBP",
        null=True,
        blank=True,
    )
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = _('Story Category')
        verbose_name_plural = _('Story Categories')

    def __str__(self):
        return self.title


class Banners(AbstractPublicModel):
    background = ProcessedImageField(
        verbose_name="Background Image",
        upload_to=partial(generate_unique_filename, field_name='title', upload_to='banners'),
        processors=[ResizeToFit(1024, 1024)],
        options={"quality": 90},
        validators=[validate_file_extension],
        format="WEBP",
        null=True,
        blank=True,
    )
    left_image = ProcessedImageField(
        verbose_name="Left Image",
        upload_to=partial(generate_unique_filename, field_name='title', upload_to='pages', custom_prefix='left-image'),
        processors=[ResizeToFit(1920, 800)],
        options={"quality": 90},
        validators=[validate_file_extension],
        format="WEBP",
        null=True,
        blank=True,
    )
    right_image = ProcessedImageField(
        verbose_name="Left Image",
        upload_to=partial(generate_unique_filename, field_name='title', upload_to='pages', custom_prefix='right-image'),
        processors=[ResizeToFit(1920, 800)],
        options={"quality": 90},
        validators=[validate_file_extension],
        format="WEBP",
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ['order']

    def __str__(self):
        return self.title
