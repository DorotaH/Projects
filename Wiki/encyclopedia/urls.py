from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("submit/", views.submit, name="submit"),
    path("newPage/", views.newPage, name="newPage"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("random/", views.random, name="random")
]
