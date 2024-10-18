from typing import Any

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import BlogPost as Blog

# Create your views here.


class BlogListView(ListView):
    model = Blog
    template_name = "blog/blog_list.html"

    paginate_by = 4

    def get_queryset(self) -> Any:
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"

    def get_context_data(self, **kwargs) -> Any:
        context = super().get_context_data(**kwargs)
        if self.object.is_published:
            self.object.view_count += 1
            self.object.save()
        return context


class BlogCreateView(CreateView):
    model = Blog
    fields = ["title", "content", "preview_image"]
    template_name = "blog/blog_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("blog", kwargs={"pk": self.object.pk})

    def form_valid(self, form) -> Any:
        # Проверяем, какую кнопку нажал пользователь
        action = self.request.POST.get("action")
        if action == "publish":
            form.instance.is_published = True  # Если выбрана публикация
        else:
            form.instance.is_published = False  # Если сохранение как черновик

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ["title", "content", "preview_image", "is_published"]
    template_name = "blog/blog_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("blog", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs) -> Any:
        context = super().get_context_data(**kwargs)
        context["blog"] = self.object
        return context

    def form_valid(self, form) -> Any:
        # Проверяем, какую кнопку нажал пользователь
        action = self.request.POST.get("action")
        if action == "publish":
            form.instance.is_published = True  # Если выбрана публикация
        else:
            form.instance.is_published = False  # Если сохранение как черновик

        return super().form_valid(form)


class BlogPublishView(View):
    def post(self, request, pk) -> Any:
        # Получаем блог по его ID
        blog = get_object_or_404(Blog, pk=pk)

        # Проверяем, опубликован ли блог
        if not blog.is_published:
            blog.is_published = True  # Устанавливаем статус "опубликован"
            blog.save()  # Сохраняем изменения
            messages.success(request, "Опубликовано")
        else:
            messages.warning(request, "Блог уже был опубликован.")

        # Перенаправляем на страницу блога после публикации
        return redirect("blog", pk=pk)


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy("blogs")  # После успешного удаления

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Блог успешно удалён.")  # Добавляем сообщение
        return super().delete(request, *args, **kwargs)
