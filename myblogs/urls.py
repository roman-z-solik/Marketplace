from django.urls import path
from myblogs.apps import BlogsConfig
from myblogs.views import BlogsListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogsConfig.name

urlpatterns = [
    path('', BlogsListView.as_view(), name='blogs_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update_blog'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),
]