from django.urls import path
from base.views.post_views import (
    post_action_view,
    post_delete_view,
    post_detail_view,
   # post_feed_view,
    post_list_view,
    post_create_view,
)


# urlpatterns = [
#     path('', views.getPosts, name="posts"),
#     path('<str:pk>/', views.getPost, name="post"),
#
# ]

urlpatterns = [
    path('', post_list_view),
    #path('feed/', tweet_feed_view),
    path('action/', post_action_view),
    path('create/', post_create_view),
    path('<str:pk>/', post_detail_view),
    path('<str:pk>/delete/', post_delete_view),
]