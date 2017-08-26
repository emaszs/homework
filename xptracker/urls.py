from django.conf.urls import url

from . import views
from django.urls.base import reverse_lazy

app_name = 'xptracker'

# TODO sort urls better!
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^developer/(?P<pk>[0-9]+)/', views.DeveloperDetailView.as_view(),
        name='developer_detail'),
    url(r'^task/(?P<pk>[0-9]+)/delete', views.TaskDeleteView.as_view(),
        name='task_delete'),
    url(r'^task/(?P<pk>[0-9]+)/', views.TaskUpdateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='task_update'),
    url(r'^story/(?P<pk>[0-9]+)/delete/', views.StoryDeleteView.as_view(),
        name='story_delete'),
    url(r'^story/create/', views.StoryCreateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='story_create'),
    url(r'^story/(?P<pk>[0-9]+)/', views.StoryUpdateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='story_update'),
    url(r'^task/create/', views.TaskCreateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='task_create'),
    url(r'^iteration/create/', views.IterationCreateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='iteration_create'),
    url(r'^work/create/task/(?P<task_id>[0-9]+)/', views.WorkCreateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='work_create'),
    url(r'^work/create/', views.WorkCreateView.as_view(
        success_url=reverse_lazy('xptracker:index')),
        name='work_create')
]
