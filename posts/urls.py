from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts_list),
    path("create/", views.create_post),
    path("<int:id>/", views.get_post),
    path("<int:id>/update/", views.update_post),
    path("<int:id>/delete/", views.delete_post),
]
