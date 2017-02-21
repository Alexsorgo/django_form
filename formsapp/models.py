from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField


class proj(models.Model):
    class Meta:
        db_table = "proj"
    project = models.CharField(max_length=100, primary_key=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.project

    def __str__(self):
        return self.project


class req(models.Model):
    class Meta:
        db_table = "req"

    url = models.URLField()
    method = models.CharField(max_length=10)
    data_form = models.CharField(max_length=10)
    header = JSONField()
    body = JSONField()
    tag = models.CharField(max_length=50, primary_key=True)
    project = models.ForeignKey(proj, related_name="req_proj")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.tag

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return "/show/%s" %(self.tag)


class res(models.Model):
    class Meta:
        db_table = "res"
    tag = models.ForeignKey(req, related_name="restag")
    status = models.CharField(max_length=50)
    body = JSONField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    project = models.ForeignKey(proj, related_name="res_proj")

    def __unicode__(self):
        return self.tag

    def __str__(self):
        return self.tag
