from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("addListing/", views.addListing, name="addListing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path('listing/<int:id>/', views.listing_view, name='listing'),
    path('listing/<int:id>/bid/', views.bid, name='bid'),
    path('listing/<int:id>/add/', views.addWatchlist, name='addWatchlist'),
    path('listing/<int:id>/remove/', views.removeWatchlist, name='removeWatchlist'),
    path('listing/<int:id>/endAuction/', views.endAuction, name='endAuction'),
    path('listing/<int:id>/comment/', views.comment, name='comment'),
    path('categories/', views.categories_view, name='categories_view'),
    path('categories/<str:name>/', views.category, name='category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

