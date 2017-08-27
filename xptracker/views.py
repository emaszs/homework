from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404

from .models import Developer, Iteration, Story, Task, Work
from django.urls.base import reverse_lazy

def index(request):
    developer_list = Developer.objects.all()
    story_list = Story.objects.all()
    task_list = Task.objects.all()
    work_list = Work.objects.all().order_by('-create_time')
    iteration_list = Iteration.objects.all()

    total_story_time_estimate = sum(story.time_hours_estimate
                                    for story in Story.objects.all())
    total_task_time_estimate = sum(task.time_hours_estimate
                                   for task in Task.objects.all())
    total_task_time_actual = sum(task.total_work for task in Task.objects.all())
    context = {'developer_list': developer_list, 'story_list': story_list,
               'task_list': task_list, 'iteration_list': iteration_list,
               'work_list': work_list,
               'total_story_time_estimate': total_story_time_estimate,
               'total_task_time_estimate': total_task_time_estimate,
               'total_task_time_actual': total_task_time_actual}

    return render(request, 'xptracker/index.html', context)


class StoryCreateView(CreateView):
    model = Story
    fields = ['name', 'iteration', 'time_hours_estimate']
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_create'

class StoryUpdateView(UpdateView):
    model = Story
    fields = ['name', 'iteration', 'time_hours_estimate']
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_update'

class StoryDeleteView(DeleteView):
    model = Story
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_delete'

class IterationCreateView(CreateView):
    model = Iteration
    fields = ['name']
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_create'

class WorkCreateView(CreateView):
    model = Work
    fields = ['name', 'time_hours', 'task', 'developer']
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_create'

    def get_initial(self):
        if 'task_id' in self.kwargs:
            task = get_object_or_404(Task, pk=self.kwargs['task_id'])
            return {'task': task}
        else:
            return {'task': None}

class DeveloperCreateView(CreateView):
    model = Developer
    fields = ['name']
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_create'

class DeveloperDetailView(DetailView):
    model = Developer

class TaskCreateView(CreateView):
    model = Task
    fields = ['name', 'story', 'developer', 'iteration',
              'time_hours_estimate']
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_create'

class TaskUpdateView(UpdateView):
    model = Task
    fields =['name', 'completed', 'developer', 'story',
             'time_hours_estimate']
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_update'

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_delete'
