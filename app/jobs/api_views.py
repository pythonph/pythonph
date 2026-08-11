"""DRF API views for the Jobs API."""

from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Company, Job
from .serializers import CompanySerializer, JobSerializer, UserSerializer


class JobPagination(PageNumberPagination):
    """Standard DRF page-number pagination for the jobs API."""

    page_size = 20


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
    pagination_class = JobPagination
    filterset_fields = ["is_approved", "is_sponsored", "is_active"]

    def get_queryset(self):
        qs = super().get_queryset()
        # Defaults: only show approved, active jobs unless explicitly filtered.
        if "is_approved" not in self.request.query_params:
            qs = qs.filter(is_approved=True)
        if "is_active" not in self.request.query_params:
            qs = qs.filter(is_active=True)
        return qs.order_by("-is_sponsored", "-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
