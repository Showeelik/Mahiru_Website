from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.is_published:
            self.object.view_count += 1
            self.object.save()
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
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

        form.instance.owner = self.request.user

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ["title", "content", "preview_image", "is_published"]
    template_name = "blog/blog_form.html"
    permission_required = "blog.change_blog"

    def has_permission(self) -> bool:
        blog = self.get_object()
        return super().has_permission() or blog.owner == self.request.user

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


class BlogPublishView(LoginRequiredMixin, View):

    def post(self, request, pk) -> Any:
        # Получаем блог по его ID
        blog = get_object_or_404(Blog, pk=pk)

        # Проверяем, опубликован ли блог
        if not blog.is_published:
            blog.publish()
            messages.success(request, "Опубликовано")
        else:
            messages.warning(request, "Блог уже был опубликован.")

        # Перенаправляем на страницу блога после публикации
        return redirect("blog", pk=pk)


class BlogUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "blog.can_unpublish_blog"

    def has_permission(self) -> bool:
        blog = get_object_or_404(Blog, pk=self.kwargs["pk"])
        return super().has_permission() or self.request.user == blog.owner

    def post(self, request, pk) -> Any:
        # Получаем блог по его ID
        blog = get_object_or_404(Blog, pk=pk)

        # Проверяем, опубликован ли блог
        if blog.is_published:
            blog.unpublish()
            messages.success(request, "Блог успешно снят с публикации.")
        else:
            messages.warning(request, "Блог уже снят с публикации.")

        # Перенаправляем на страницу блога после снятия с публикации
        return redirect("blog", pk=pk)


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("blogs")  # После успешного удаления
    permission_required = "blog.delete_blog"

    def has_permission(self) -> bool:
        blog = self.get_object()
        return super().has_permission() or blog.owner == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Блог успешно удалён.")  # Добавляем сообщение
        return super().delete(request, *args, **kwargs)
