from django import forms
import unrest_schema

from .models import Task, Project, Activity


class OwnerForm(forms.ModelForm):
    user_can_POST = 'AUTH'
    user_can_PUT = 'OWN'
    def save(self, *args, **kwargs):
        self.instance.user = self.request.user
        return super().save(*args, **kwargs)


@unrest_schema.register
class ProjectForm(OwnerForm):
    readonly_fields = ['slug']
    class Meta:
        model = Project
        fields = ('name', 'data')


@unrest_schema.register
class ActivityForm(OwnerForm):
    readonly_fields = ['slug']
    class Meta:
        model = Activity
        fields = ('name', 'data', 'project')


@unrest_schema.register
class TaskForm(OwnerForm):
    readonly_fields = ['slug']
    filter_fields = ['activity_id']
    class Meta:
        model = Task
        fields = ('name', 'completed', 'data', 'project', 'activity')

    def save(self, *args, **kwargs):
        self.instance.data = self.instance.data or {}
        instance = super().save(*args, **kwargs)
        if self.request_data.get('add_activity'):
            activity, new = Activity.objects.get_or_create(name=instance.name)
            instance.activity = activity
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['completed'].required = False
        self.fields['project'].required = False
        self.fields['activity'].required = False
