from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name = 'home'),
    path('proj1', views.proj1,name = 'project-1'),
    path('proj2', views.proj2,name="project-2"),
    path('post/', views.post_view, name='post_view'),
]


