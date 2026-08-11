"""DRF serializers for the Jobs API."""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Company, Job


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "name"]

    def get_name(self, obj):
        return obj.get_full_name()


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ["id", "user", "name", "profile", "homepage", "created_at", "updated_at"]


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "user",
            "company",
            "title",
            "salary_range",
            "short_description",
            "description",
            "location",
            "is_remote",
            "application_url",
            "application_email",
            "is_approved",
            "is_sponsored",
            "is_active",
            "created_at",
            "updated_at",
        ]
