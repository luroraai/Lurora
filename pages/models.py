from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from tinymce.models import HTMLField
from wosvcore.absmodel import AbstractPublicModel, AbstractCoreModel, AbstractContentModel
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill, SmartResize
from wosvcore.utils import validate_file_extension, generate_unique_filename
from functools import partial


class Pages(AbstractContentModel, MPTTModel):
    PAGE_TYPES = (
        ('page', 'Sayfa'),
        ('home', 'Home'),
        ('about', 'About'),
        ('contact', 'Contact'),
        ('stories', 'Stories'),
        ('faq', 'FAQ'),
        ('terms', 'Terms and Conditions'),
        ('privacy', 'Privacy Policy'),
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name=_('Slug'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Parent Page'))
    image_path = ProcessedImageField(
        verbose_name="Page Image",
        upload_to=partial(generate_unique_filename, field_name='title', upload_to='pages'),
        processors=[ResizeToFit(1024, 1024)],
        options={"quality": 90},
        validators=[validate_file_extension],
        format="WEBP",
        null=True,
        blank=True,
    )
    header_image = ProcessedImageField(
        verbose_name="Header Image",
        upload_to=partial(generate_unique_filename, field_name='title', upload_to='pages', custom_prefix='header-image'),
        processors=[ResizeToFit(1920, 800)],
        options={"quality": 90},
        validators=[validate_file_extension],
        format="WEBP",
        null=True,
        blank=True,
    )
    alt_url = models.URLField(blank=True, null=True, verbose_name=_('Alternative URL'))
    visible_home = models.BooleanField(default=False, verbose_name=_('Visible on Homepage'))
    visible_header = models.BooleanField(default=False, verbose_name=_('Visible in Header'))
    visible_footer = models.BooleanField(default=False, verbose_name=_('Visible in Footer'))
    page_type = models.CharField(max_length=40, choices=PAGE_TYPES, verbose_name=_('Page Type'), default=PAGE_TYPES[0])
    sort_order = models.PositiveIntegerField(verbose_name=_("Sıralama"), default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.page_type == self.PAGE_TYPES[1][0]:
            return reverse('pages:index')
        else:
            return reverse('pages:detail', args=[self.slug])

    def get_image_url(self):
        if self.image_path:
            return self.image_path.url
        else:
            return ''


class Contents(AbstractContentModel, MPTTModel):
    CONTENT_TYPES = (
        ('text', 'Text'),
        ('card', 'Card'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('link', 'Link'),
        ('accordion', 'Accordion'),
        ('tab_segment', 'Tab Segment'),
    )
    VIDEO_TYPES = (
        ('youtube', 'Youtube'),
        ('vimeo', 'Vimeo'),
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Parent Content'))
    page = models.ForeignKey(Pages, on_delete=models.CASCADE, verbose_name=_('Page'))
    image_path = ProcessedImageField(
        verbose_name="Image",
        upload_to=partial(generate_unique_filename, field_name='title', upload_to='pages', custom_prefix='content-image'),
        processors=[ResizeToFit(1024, 1024)],
        options={"quality": 90},
        validators=[validate_file_extension],
        format="WEBP",
        null=True,
        blank=True,
    )
    alt_url = models.URLField(blank=True, null=True, verbose_name=_('Alternative URL'))
    visible_home = models.BooleanField(default=False, verbose_name=_('Visible on Homepage'))
    video_type = models.CharField(max_length=50, choices=VIDEO_TYPES, verbose_name=_('Video Type'))
    video_url = models.URLField(verbose_name=_('Video URL'))
    video_thumb_url = models.URLField(blank=True, null=True, verbose_name=_('Video Thumbnail URL'))
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES, verbose_name=_('Content Type'), default=CONTENT_TYPES[0])
    sort_order = models.PositiveIntegerField(verbose_name=_("Sıralama"), default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

    def get_image_url(self):
        if self.image_path:
            return self.image_path.url


class Images(AbstractPublicModel):
    image_path = ProcessedImageField(
        verbose_name="Image",
        upload_to=partial(generate_unique_filename, field_name='title', upload_to='pages', custom_prefix='page-image'),
        processors=[ResizeToFit(1024, 1024)],
        options={"quality": 90},
        validators=[validate_file_extension],
        format="WEBP",
        null=True,
        blank=True,
    )
