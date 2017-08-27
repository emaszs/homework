from django.conf.urls import url

from . import views

app_name = 'xptracker'

# TODO sort urls better!
urlpatterns = [
    # ex: /xptracker/
    url(r'^$', views.index, name='index'),
    # ex: /developer/5/
    url(r'^developer/(?P<pk>[0-9]+)/', views.DeveloperDetailView.as_view(),
        name='developer_detail'),
    # ex: /developer/create/
    url(r'^developer/create/', views.DeveloperCreateView.as_view(),
        name='developer_create'),
    # ex: /task/5/delete/
    url(r'^task/(?P<pk>[0-9]+)/delete', views.TaskDeleteView.as_view(),
        name='task_delete'),
    # ex: /task/5/
    url(r'^task/(?P<pk>[0-9]+)/', views.TaskUpdateView.as_view(),
        name='task_update'),
    # ex: /story/5/delete/
    url(r'^story/(?P<pk>[0-9]+)/delete/', views.StoryDeleteView.as_view(),
        name='story_delete'),
    # ex: /story/create/
    url(r'^story/create/', views.StoryCreateView.as_view(),
        name='story_create'),
    # ex: /story/5/
    url(r'^story/(?P<pk>[0-9]+)/', views.StoryUpdateView.as_view(),
        name='story_update'),
    # ex: /task/create/
    url(r'^task/create/', views.TaskCreateView.as_view(),
        name='task_create'),
    # ex: /iteration/create/
    url(r'^iteration/create/', views.IterationCreateView.as_view(),
        name='iteration_create'),
    # ex: /work/create/task/5/
    url(r'^work/create/task/(?P<task_id>[0-9]+)/',
        views.WorkCreateView.as_view(),
        name='work_create'),
    # ex: /work/create/
    url(r'^work/create/', views.WorkCreateView.as_view(),
        name='work_create'),
]
