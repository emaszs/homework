from django.conf.urls import url

from . import views
from django.urls.base import reverse_lazy

app_name = 'xptracker'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^developer/(?P<pk>[0-9]+)/', views.DeveloperDetailView.as_view(),
        name='developer_detail'),
    url(r'^task/(?P<pk>[0-9]+)/', views.TaskUpdateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='task_update'),
    url(r'^story/create/', views.StoryCreateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='story_create'),
    url(r'^task/create/', views.TaskCreateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='task_create'),
    url(r'^iteration/create/', views.IterationCreateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='iteration_create'),
]
