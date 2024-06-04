
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import IndexView, LoginView, LogoutView, RegisterView, FollowingView, ProfileView, EditView, FollowView, ManageLikesView

from . import views

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register", RegisterView.as_view(), name="register"),
    path("following", FollowingView.as_view(), name="following"),
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    
    path("edit/<int:post_id>", EditView.as_view(), name="edit"),
    path("profile/<str:username>/follow/", FollowView.as_view(), name="follow"),
    path("likes/<int:post_id>", ManageLikesView.as_view(), name="likes"),
]
