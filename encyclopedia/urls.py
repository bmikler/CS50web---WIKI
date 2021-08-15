from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"), 
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random_page")
]
