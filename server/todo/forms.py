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
class TaskForm(OwnerForm):
    class Meta:
        model = Task
        fields = ('name', 'due', 'completed', 'data')

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if self.request.data.get('add_activity'):
            activity, new = Activity.objects.get_or_create(name=instance.name)
            instance.activity = activity
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due'].required = False
        self.fields['completed'].required = False
