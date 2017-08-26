from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Developer, Iteration, Story, Task, Work
from django.urls.base import reverse_lazy

def index(request):
    developer_list = Developer.objects.all()
    story_list = Story.objects.all()
    task_list = Task.objects.all()
    iteration_list = Iteration.objects.all()
    incomplete_task_list = task_list.filter(completed=False)
    total_story_time_estimate = sum(story.time_hours_estimate
                                    for story in Story.objects.all())
    total_task_time_estimate = sum(task.time_hours_estimate
                                   for task in Task.objects.all())
    total_task_time_actual = sum(task.total_work for task in Task.objects.all())
    context = {'developer_list': developer_list, 'story_list': story_list,
               'task_list': task_list, 'iteration_list': iteration_list,
               'incomplete_task_list': incomplete_task_list,
               'total_story_time_estimate': total_story_time_estimate,
               'total_task_time_estimate': total_task_time_estimate,
               'total_task_time_actual': total_task_time_actual}

    return render(request, 'xptracker/index.html', context)
#     return HttpResponse("This should be the main page where we display<br />"
#         "all stories (their time estimate and actual work time)<br />"
#         "all tasks (also their time estimate and actual work time<br />"
#         "all iterations (with links we can filter tasks and stories"
#         "displayed by the specific iteration<br />")

#TODO have ability to take tasks from other developers
# Have a display for current iteration with unassigned tasks and maybe developers
# with the most work.





def task(request, task_id):
    """
    Task details (and modification form for everything):
        name
        description
        developer
        time estimate (entered when creating a task? maybe should
            be entered by the developer?)
        time actually spent on this task
        story which it belongs to, also which iteration
        list of developers, comparison of their workloads by time of tasks
            undertaken?
    """

def story(request, story_id):
    """
    Story details (and modification form):
        name
        description
        list of tasks which make up this story
        time estimate as a sum of task time estimates
        time spent as a sum of time spent on subtasks
    """

def iteration(request, iteration_id):
    """
    Iteration details (and modification form):
        name
    """

# def developer_detail(request, developer_id):
#     """
#     developer details?
#         name
#         tasks currently taken
#         tasks completed?
#     """

class StoryCreateView(CreateView):
    model = Story
    fields = ['name', 'description', 'iteration', 'time_hours_estimate']
    template_name_suffix = '_create'

class StoryUpdateView(UpdateView):
    model = Story
    fields = ['name', 'description', 'iteration', 'time_hours_estimate']
    template_name_suffix = '_update'

class StoryDeleteView(DeleteView):
    model = Story
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_delete'

class IterationCreateView(CreateView):
    model = Iteration
    fields = ['name']
    template_name_suffix = '_create'

# TODO add custom form with ability to complete a task when submitting work!
class WorkCreateView(CreateView):
    model = Work
    fields = ['name', 'description', 'time_hours', 'task', 'developer']
    template_name_suffix = '_create'

    def get_initial(self):
        if 'task_id' in self.kwargs:
            task = get_object_or_404(Task, pk=self.kwargs['task_id'])
            return {'task': task}
        else:
            return {'task': None}

class DeveloperDetailView(DetailView):
    model = Developer

class TaskCreateView(CreateView):
    model = Task
    fields = ['name', 'description', 'story', 'developer', 'iteration',
              'time_hours_estimate']
    template_name_suffix = '_create'

class TaskUpdateView(UpdateView):
    model = Task
    fields =['name', 'description', 'completed', 'developer', 'story',
             'time_hours_estimate']
    template_name_suffix = '_update'

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('xptracker:index')
    template_name_suffix = '_delete'

# def work_create(request):
#     if request.method == "POST":
#         form = WorkCreateForm(request)
#         if form.is_valid():
#             return HttpResponseRedirect('/lol/')
#     else:
#         form = WorkCreateForm()
#
#     return render(request, 'xptracker/work_create.html', {'form': form})

# class WorkCreateView(TemplateView):
#     template_name = 'work_create.html'
#
#     def get(self, request, *args, **kwargs):
#         work_create_form = WorkCreateForm()
#         WorkTaskFormSet = inlineformset_factory(Work, Task)
#         formset = WorkTaskFormSet()
#
#         context = {'form': work_create_form, 'formset': formset}
#         return self.render_to_response(context)


