from django.urls import path

from .views import LoginView, LogoutView, ProfileDeleteView, ProfileEditView, ProfileView, RegisterView

urlpatterns = [
    path("login", view=LoginView.as_view(), name="login"),
    path("logout", view=LogoutView.as_view(next_page="home"), name="logout"),
    path("signup", view=RegisterView.as_view(), name="signup"),
    path("profile", view=ProfileView.as_view(), name="profile"),
    path("profile/edit", view=ProfileEditView.as_view(), name="profile-edit"),
    path("profile/delete", view=ProfileDeleteView.as_view(), name="profile-delete"),
]
