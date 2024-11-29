from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts_list),
    path("create/", views.create_post),
    path("<int:id>/", views.get_post),
    path("<int:id>/update/", views.update_post),
    path("<int:id>/delete/", views.delete_post),
    path("<int:id>/comments/", views.get_comment),
    path("<int:id>/comment/", views.create_comment),
    path("comment/<int:comment_id>/", views.update_comment),
    path("comment/<int:comment_id>/delete/", views.delete_comment),
    path("<int:id>/like/", views.like_post),
]
