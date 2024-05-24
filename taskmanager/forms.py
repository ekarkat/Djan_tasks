from django import forms

from .models import Workspace, Unit, Task


# forms for the models in the taskmanager app

class WorkSpaceForm(forms.ModelForm):
    # workspace form with title and description fields

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WorkSpaceForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Workspace
        fields = ['title', 'description']

class UnitForm(forms.ModelForm):
    # unit form with title and description fields

    class Meta:
        model = Unit
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    # task form with title, description, deadline, addressed_to and priority fields

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'priority']
