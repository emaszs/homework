from django.forms import ModelForm

from .models import Work

class WorkCreateForm(ModelForm):
    class Meta:
        model = Work
        fields =['name', 'description', 'task', 'time_hours']
