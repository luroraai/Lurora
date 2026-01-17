#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 25.03.2025 21:17
#  Filename : abschoices.py
#  Last Modified : 25.03.2025 21:17
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
from django.db import models
from enum import Enum
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    ACTIVE = 'active', _('Active')
    INACTIVE = 'inactive', _('Inactive')
    PENDING = 'pending', _('Pending')
    ARCHIVED = 'archived', _('Archived')
    CANCELLED = 'cancelled', _('Cancelled')
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')
    COMPLETED = 'completed', _('Completed')
    PUBLISHED = 'published', _('Published')
    DRAFT = 'draft', _('Draft')
