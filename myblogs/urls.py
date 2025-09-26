from django.urls import path
from myblogs.apps import BlogsConfig
from myblogs.views import BlogsListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogsConfig.name

urlpatterns = [
    path('', BlogsListView.as_view(), name='blogs_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='create_blog'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='update_blog'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='delete_blog'),
]