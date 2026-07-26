"""DRF API views for the Jobs API — replaces Tastypie resources.

Maintains the same filtering and ordering behavior as the old Tastypie API.
"""

from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Company, Job
from .serializers import CompanySerializer, JobSerializer, UserSerializer


class TastypieCompatiblePagination(PageNumberPagination):
    """Paginator that matches Tastypie's response format:

    { "objects": [...], "meta": { "next": ..., "previous": ... } }
    """

    page_size = 20

    def get_paginated_response(self, data):
        return Response(
            {
                "objects": data,
                "meta": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }
        )


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CompanyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    pagination_class = TastypieCompatiblePagination
    filterset_fields = ["is_approved", "is_sponsored"]

    def get_queryset(self):
        qs = super().get_queryset()
        # Default: only show approved jobs (matches old Tastypie build_filters)
        if "is_approved" not in self.request.query_params:
            qs = qs.filter(is_approved=True)
        return qs.order_by("-is_sponsored", "-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
