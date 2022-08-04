from django.forms import ModelForm
from jobs.models import Company, Job


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ["user"]


class JobForm(ModelForm):
    class Meta:
        model = Job
        exclude = [
            "tags",
            "user",
            "company",
            "is_approved",
            "is_sponsored",
            "is_active",
        ]
