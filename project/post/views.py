from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny 
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostListSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer
    
    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        elif self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
    
    @action(methods=["GET"], detail=False)
    def recommend(self, request):
        ran_post = self.get_queryset().order_by("?").first()
        ran_post_serializer = PostListSerializer(ran_post)
        return Response(ran_post_serializer.data)
    
    @action(methods=["GET"], detail=True)
    def test(self, request, pk=None):
        test_post = self.get_object()
        test_post.like_num += 1
        test_post.save(update_fields=["like_num"])
        return Response()

    @action(methods=["GET"], detail=False)
    def top_liked(self, request):
        top_posts = Post.objects.order_by('-like_num')[:3]
        top_posts_serializer = self.get_serializer(top_posts, many=True)
        return Response(top_posts_serializer.data)

    '''
    serializer_class = PostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        post = serializer.save()
    '''
    
class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        elif self.action in ["retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]
    
class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    #queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id=post)
        return queryset
    '''
    def list(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        queryset = self.filter_queryset(self.get_queryset().filter(post=post))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    '''
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, writer=request.user)
        return Response(serializer.data)
    