# -*- coding: utf-8 -*-

from django.db import models
import datetime


class Art(models.Model):
    title = models.CharField(max_length=255, blank=True , null=True)
    book_name = models.CharField(max_length=255, blank=True , null=True)
    page = models.CharField(max_length=255, blank=True , null=True)
    author_name = models.CharField(max_length=255, blank=True , null=True)
    mail = models.CharField(max_length=255, blank=True , null=True)
    link = models.CharField(max_length=255, blank=True , null=True)
    time = models.DateTimeField(auto_now_add=True)

    def time_str(self):
        return self.time.strftime("%Y-%m-%d")



class Read(models.Model):
    url = models.CharField(max_length=255, blank=True , null=True)



class Collected(models.Model):
    url = models.CharField(max_length=255, blank=True , null=True)
        


