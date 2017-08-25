from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Developer, Iteration, Story, Task

def index(request):
    developer_list = Developer.objects.all()
    story_list = Story.objects.all()
    task_list = Task.objects.all()
    iteration_list = Iteration.objects.all()
    context = {'developer_list': developer_list, 'story_list': story_list,
               'task_list': task_list, 'iteration_list': iteration_list}

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
    fields = ['name', 'description', 'iteration']
    template_name_suffix = '_create'

class TaskCreateView(CreateView):
    model = Task
    fields =['name', 'description', 'story', 'developer']
    template_name_suffix = '_create'

# TODO validation date validation! dates should not overlap!
class IterationCreateView(CreateView):
    model = Iteration
    fields = ['name', 'date_start', 'date_end']
    template_name_suffix = '_create'


class DeveloperDetailView(DetailView):
    model = Developer

class TaskUpdateView(UpdateView):
    model = Task
    fields =['developer']
    template_name_suffix = '_update'

