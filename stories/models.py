from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse


class Stories(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('failed', 'Failed')
    ]

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    topic = models.CharField(max_length=200, verbose_name=_("Topic"))
    scene_count = models.PositiveIntegerField(default=1, verbose_name=_("Scenes"))
    cover_image = models.ImageField(upload_to='stories/', verbose_name=_("Cover Image"))
    story_image = models.ImageField(upload_to='stories/', verbose_name=_("Story Image"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    content = models.TextField(verbose_name=_("Content"), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Author"), related_name='stories')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft', verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'

    def get_image_url(self):
        if self.scenes.all().count() > 0 and self.scenes.first().generated_image:
            return self.scenes.first().get_generated_image_url()
        return settings.STATIC_URL + 'common/img/banner2.webp'

    def get_all_images(self):
        return [scene.get_generated_image_url() for scene in self.scenes.all()]

    def get_absolute_url(self):
        return reverse('accounts:stories:detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('accounts:stories:edit', args=[self.pk])

    def get_delete_url(self):
        return reverse('accounts:stories:delete', args=[self.pk])

    # def get_publish_url(self):
    #     return reverse('accounts:stories:publish', args=[self.pk])

    def set_status(self, status):
        self.status = status
        self.save()

    def has_scenes(self):
        return self.scenes.all().count() > 0

    def has_content(self):
        return self.content is not None and self.content != False


class Scenes(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name='scenes', verbose_name=_("Story"))
    scene_title = models.CharField(max_length=200, verbose_name=_("Scene Title"), blank=True, null=True)
    scene_number = models.PositiveIntegerField(verbose_name=_("Scene Number"), default=1)
    content = models.TextField(verbose_name=_("Content"), blank=True, null=True)
    gen_content = models.TextField(blank=True, null=True, verbose_name=_("Generate Content"))
    generated_image = models.ImageField(upload_to='generated_images/', blank=True, null=True, verbose_name=_("Generated Image"))
    scene_image = models.ImageField(upload_to='scenes/', blank=True, null=True, verbose_name=_("Scene Image"))
    image_url = models.TextField(blank=True, null=True, verbose_name=_("Image URL"))
    keyword = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Keyword"))
    question = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Question"))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"Scene {self.scene_number} of {self.story.title}"

    class Meta:
        ordering = ['scene_number']
        verbose_name_plural = 'Scenes'

    def get_generated_image_url(self):
        return self.generated_image.url if self.generated_image else settings.STATIC_URL + 'common/img/banner.webp'

    def get_img_url(self):
        return self.image_url if self.image_url else None

    def get_image_url(self):
        return self.scene_image.url if self.scene_image else None
