from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from myblogs.models import Blog


class BlogsListView(ListView):
    model = Blog
    template_name = 'blogs_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publication_sign=True)


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    template_name = 'create_blog.html'
    fields = ("title", "content", "image", "publication_sign")
    success_url = reverse_lazy('blogs:blogs_list')


class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'update_blog.html'
    fields = ("title", "content", "image", "publication_sign")
    success_url = reverse_lazy('blogs:blogs_list')

    def get_success_url(self):
        return reverse('blogs:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'confirm_delete_blog.html'
    success_url = reverse_lazy('blogs:blogs_list')