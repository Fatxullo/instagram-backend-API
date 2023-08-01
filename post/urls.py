from django.urls import path
from .views import (
    PostListApiView,
    PostCreateView,
    PostRetrieveUpdateDestroyView,
    PostCommentListView,
    PostCommentCreateView,
    CommentListCreateApiView,
    PostLikeListView,
    CommentRetrieveView,
    CommnetLikeListView,
    PostLikeView,
    CommentLikeView
)



urlpatterns = [
    path('list/', PostListApiView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('<uuid:pk>/likes/', PostLikeListView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListView.as_view()),
    path('<uuid:pk>/comments/create/', PostCommentCreateView.as_view()),
    path('comments/create/', CommentListCreateApiView.as_view()),
    path('comments/<uuid:pk>/', CommentRetrieveView.as_view()),
    path('comments/<uuid:pk>/likes/', CommnetLikeListView.as_view()),
    path('<uuid:pk>/create-delete-like/', PostLikeView.as_view()),
    path('comments/<uuid:pk>/create-delete-like/', CommentLikeView.as_view())
]
