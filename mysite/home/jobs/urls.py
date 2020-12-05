from django.urls import path, reverse_lazy
from . import views
from django.conf.urls import url
from django.views.static import serve
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app_name='jobs'
urlpatterns = [
    path('', views.JobListView.as_view()),
    path('jobs', views.JobListView.as_view(), name='all'),
    path('job/<int:pk>', views.JobDetailView.as_view(), name='job_detail'),
    path('job/create',
        views.JobCreateView.as_view(success_url=reverse_lazy('jobs:all')), name='job_create'),
    path('job/<int:pk>/update',
        views.JobUpdateView.as_view(success_url=reverse_lazy('jobs:all')), name='job_update'),
    path('job/<int:pk>/delete',
        views.JobDeleteView.as_view(success_url=reverse_lazy('jobs:all')), name='job_delete'),
        
    path('employer/', views.EmployerListView.as_view(), name='employer_list'),
    path('employer/create/', views.EmployerCreateView.as_view(), name='employer_create'),
    path('employer/<int:pk>/update/', views.EmployerUpdateView.as_view(), name='employer_update'),
    path('employer/<int:pk>/delete/', views.EmployerDeleteView.as_view(), name='employer_delete'),
    # path('title/', views.EmployerListView.as_view(), name='title_list'),
    # path('title/create/', views.EmployerCreateView.as_view(), name='title_create'),
    # path('title/<int:pk>/update/', views.EmployerUpdateView.as_view(), name='title_update'),
    # path('title/<int:pk>/delete/', views.EmployerDeleteView.as_view(), name='title_delete'),
    path('location/', views.EmployerListView.as_view(), name='location_list'),
    path('location/create/', views.EmployerCreateView.as_view(), name='location_create'),
    path('location/<int:pk>/update/', views.EmployerUpdateView.as_view(), name='location_update'),
    path('location/<int:pk>/delete/', views.EmployerDeleteView.as_view(), name='location_delete'),

    # path('job_picture/<int:pk>', views.stream_file, name='job_picture'),
    path('job/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='job_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('jobs:all')), name='job_comment_delete'),
    path('job/<int:pk>/favorite',
       views.JobdFavoriteView.as_view(), name='job_favorite'),
    path('job/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='job_unfavorite'),


    url(r'^static/(?P<path>.*)$', serve,
    {'document_root': os.path.join(BASE_DIR, 'static'), 'show_indexes': True},
    name='static'
)
]