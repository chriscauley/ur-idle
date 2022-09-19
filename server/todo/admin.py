from django.contrib import admin

from .models import Project, Activity, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
