from django.db import models
import misaka
from django.urls import reverse
from django.utils.text import slugify

from django.contrib.auth import get_user_model

User = get_user_model()

from django import template
register = template.Library()


class Group(models.Model):
    name = models.CharField(verbose_name='Thread name', unique=True, max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField(default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Completes the attribures 'slug' and 'description_html' and saves the group to a database
        """
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Built-in django method that compiles a URL for a created group.
        """
        return reverse('groups:single', kwargs={'slug': self.slug})


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='membership')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
