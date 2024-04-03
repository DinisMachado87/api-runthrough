from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly

from .models import Profile


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        # get all profiles that are followed by a profile, given its id
        'owner__followed__owner__profile',

    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

    # def get(self, request):
    #     profiles = Profile.objects.all()
    #     serializer = ProfileSerializer(
    #         profiles,
    #         many=True,
    #         context={'request': request}
    #         )
    #     return Response(serializer.data)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()

    # serializer_class = ProfileSerializer
    #     permission_classes = [IsOwnerOrReadOnly]

    #     def get_object(self, pk):
    #         try:
    #             return Profile.objects.get(pk=pk)
    #         except Profile.DoesNotExist:
    #             raise Http404

    #     def get(self, request, pk):
    #         profile = self.get_object(pk)
    #         self.check_object_permissions(request, profile)
    #         serializer = ProfileSerializer(
    #             profile,
    #             context={'request': request}
    #             )
    #         return Response(serializer.data)

    #     def put(self, request, pk):
    #         profile = self.get_object(pk)
    #         serializer = ProfileSerializer(
    #             profile,
    #             data=request.data,
    #             context={'request': request}
    #             )
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #             )
