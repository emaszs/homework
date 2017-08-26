from django.contrib import admin

from .models import Developer, Iteration, Task, Story, Work

# Register your models here.
admin.site.register([Developer, Iteration, Task, Story, Work])
