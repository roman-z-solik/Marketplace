from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from myblogs.models import Blog


class BlogsListView(ListView):
    """BlogsListView - это класс на основе представления (view) в Django,
    который наследуется от ListView и предназначен для отображения списка блогов."""

    model = Blog
    template_name = "blogs_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publication_sign=True)


class BlogDetailView(DetailView):
    """BlogDetailView - это класс на основе представления (DetailView) в Django,
    предназначенный для отображения детальной информации о конкретном блоге с
    автоматическим подсчетом просмотров."""

    model = Blog
    template_name = "blog_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    """BlogCreateView - это класс на основе представления (CreateView) в Django,
    предназначенный для создания новых записей блога через веб-интерфейс."""

    model = Blog
    template_name = "create_blog.html"
    fields = ("title", "content", "image", "publication_sign")
    success_url = reverse_lazy("myblogs:blogs_list")


class BlogUpdateView(UpdateView):
    """BlogUpdateView - это класс на основе представления (UpdateView) в Django,
    предназначенный для редактирования существующих записей блога. После успешного
    обновления перенаправляет на детальную страницу этого же блога"""

    model = Blog
    template_name = "update_blog.html"
    fields = ("title", "content", "image", "publication_sign")
    success_url = reverse_lazy("myblogs:blogs_list")

    def get_success_url(self):
        return reverse("myblogs:blog_detail", args=[self.kwargs.get("pk")])


class BlogDeleteView(DeleteView):
    """BlogDeleteView - это класс на основе представления (DeleteView) в Django,
    предназначенный для удаления записей блога с подтверждением действия."""

    model = Blog
    template_name = "delete_blog.html"
    success_url = reverse_lazy("myblogs:blogs_list")
