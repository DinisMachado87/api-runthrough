from django.db.models import Count
from django.http import Http404
from rest_framework import status, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('created_at')
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        # User feed - Filter by followed users
        'owner__followed__owner__profile',
        # Filter by liked posts
        'likes__owner__profile',
        # user profile - Filter by user's posts
        'owner__profile'
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'created_at',
    ]
    search_fields = [
        'title',
        'owner__username',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # serializer_class = PostSerializer
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly
    #     ]
    # def get(self, request):
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(
    #         posts, many=True,
    #         context={'request': request}
    #         )
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = PostSerializer(
    #         data=request.data,
    #         context={'request': request}
    #         )

    #     if serializer.is_valid():
    #         serializer.save(owner=request.user)
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_201_CREATED
    #             )
    #     return Response(
    #         Response.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #         )


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('created_at')
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # permission_classes = [IsOwnerOrReadOnly]
    # serializer_class = PostSerializer

    # def get_object(self, pk):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, post)
    #         return post
    #     except Post.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(
    #         post,
    #         context={'request': request}
    #         )
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(
    #         post,
    #         data=request.data,
    #         context={'request': request}
    #         )

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #         )

    # def delete(self, request, pk):
    #     post = self.get_object(pk)
    #     post.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
