from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('home/', PostListView.as_view(), name='post_list'),
    path("home/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("home/new/", PostCreateView.as_view(), name="post_form"),
    path("home/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("home/<int:pk>/delete/", PostDeleteView.as_view(), name="post_confirm_delete"),
]
