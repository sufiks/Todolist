from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from goals.serializers import GoalCategoryCreateSerializer
from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, GenericAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView
from goals.models import GoalCategory
from goals.serializers import GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer

class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend]
    # filterset_fields = ["board"]

    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        instance.save(update_fields=('is_deleted',))
        return instance

