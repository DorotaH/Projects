from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    # API
    path("reset/", views.ResetView.as_view(), name="reset"),
    path(
        "generateWorld/",
        views.GenerateWorldView.as_view(),
        name="generateWorld",
    ),
    path("factory/", views.FactoryView.as_view(), name="factory"),
    path("factory/bearers/", views.BearersView.as_view(), name="bearers"),
    path("fence/", views.FenceView.as_view(), name="fence"),
    path("song/", views.SongView.as_view(), name="song"),
    path("coding/", views.CodingView.as_view(), name="coding"),
    path("guards/", views.GuardsView.as_view(), name="guards"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
