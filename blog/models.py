from django.db import models


# Create your models here.
class BlogPost(models.Model):
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE, verbose_name="Владелец")
    title = models.CharField(max_length=200)
    content = models.TextField()
    preview_image = models.ImageField(upload_to="previews/")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0, editable=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        permissions = [
            ("can_unpublish_blog", "Can unpublish blog"),
            ("delete_blog", "Can delete blog"),
        ]

    def unpublish(self):
        self.is_published = False
        self.save()

    def publish(self):
        self.is_published = True
        self.save()
