from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.wiki, name="wiki"),
    path("wiki/<str:title>/", views.title, name="title"),
    path("createpage", views.createpage, name="createpage"),
    path("entries", views.entries, name="entry"),
    path("edit", views.edit, name="edit"),
    path("save", views.save_entries, name="save_entries"),
    path("random", views.random, name="random")
]
