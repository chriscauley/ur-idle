from django.conf import settings
from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    class Meta:
        abstract = True
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)
    data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)


class Project(BaseModel):
    # largest grouping of tasks and activities (eg home, work, exercise)
    class Meta:
        ordering = ('name',)


class Activity(BaseModel):
    # settings for repeatable tasks (eg clean dishes, specific exercises)
    class Meta:
        ordering = ('-created',)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(BaseModel):
    # a thing a user should do and a record of it's completion
    class Meta:
        ordering = ('-created',)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    due = models.DateTimeField()
    completed = models.DateTimeField(null=True, blank=True)