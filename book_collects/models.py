
# -*- coding: utf-8 -*-
from django.db import models
class Info(models.Model):
    uid = models.CharField(max_length=64, blank=True , null=True)
    key = models.CharField(max_length=64, blank=True , null=True)
    value = models.CharField(max_length=255, blank=True , null=True)
