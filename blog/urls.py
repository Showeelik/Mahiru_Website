from django.urls import path

from .views import BlogCreateView, BlogDeleteView, BlogDetailView, BlogListView, BlogPublishView, BlogUpdateView

urlpatterns = [
    path("blogs", BlogListView.as_view(), name="blogs"),
    path("blog/<int:pk>", BlogDetailView.as_view(), name="blog"),
    path("blog/new", BlogCreateView.as_view(), name="blog-create"),
    path("blog/<int:pk>/edit", BlogUpdateView.as_view(), name="blog-update"),
    path("blog/<int:pk>/delete", BlogDeleteView.as_view(), name="blog-delete"),
    path("blog/<int:pk>/publish", BlogPublishView.as_view(), name="blog-publish"),
]
