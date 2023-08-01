from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, PostComment, PostLike, CommentLike
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from shared.custop_pagination import CustomPagination 





# Posts List View
class PostListApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination
    
    
    def get_queryset(self):
        return Post.objects.all()



# Create Post View
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



# Retrieve Update Delete Post
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    
    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': 'Post successefully changed.',
                'data': serializer.data,
                
            }
        )
    
    
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_204_NO_CONTENT,
                'message': 'Post successefully deleted.',
            }
        )




# Post Comment List View
class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    
    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset



# Write Comment For one Post View
class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]
     
    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)




# Comment List Create View shorter
class CommentListCreateApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = PostComment.objects.all()
    pagination_class = CustomPagination
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




# Post Likes List View
class PostLikeListView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]
    
    def get_queryset(self):
        post_id = self.kwargs['pk']
        return PostLike.objects.filter(post_id=post_id)





# Comment Retrieve View
class CommentRetrieveView(generics.RetrieveAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]
    queryset = PostComment.objects.all()



# Comment Likes View
class CommnetLikeListView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]
    
    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return CommentLike.objects.filter(comment_id=comment_id)



# Like Post View
class PostLikeView(APIView):
    
    def post(self, request, pk):
        try:
            post_like = PostLike.objects.get(
                author = self.request.user,
                post_id = pk
            )
            post_like.delete()
            data = {
                    'succuess': True,
                    'message': 'Like from this Post deleted',
                    'data': None
            }
            return Response(data, status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            post_like = PostLike.objects.create(
                author=self.request.user,
                post_id=pk
            )
            serializer = PostLikeSerializer(post_like)
            data = {
                "success": True,
                "message": "Post Liked",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)




# Comment Like View
class CommentLikeView(APIView):
    
    def post(self, request, pk):
        try:
            comment_like = CommentLike.objects.get(
                author = self.request.user,
                comment_id = pk
            )
            comment_like.delete()
            data = {
                    'succuess': True,
                    'message': 'Like from this Comment deleted',
                    'data': None
            }
            return Response(data, status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            comment_like = CommentLike.objects.create(
                author = self.request.user,
                comment_id = pk
            )
            serializer = CommentLikeSerializer(comment_like)
            data = {
                'success': True,
                'message': 'Comment Liked',
                'data': serializer.data
            }
            return Response(data, status.HTTP_201_CREATED)
            