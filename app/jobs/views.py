from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .forms import CompanyForm, JobForm
from .models import Company, Job

JOBS_PER_PAGE = 20


def index(request):
    jobs = (
        Job.objects.filter(is_approved=True, is_active=True)
        .select_related("company")
        .prefetch_related("tags")
        .order_by("-is_sponsored", "-created_at")
    )

    search_query = request.GET.get("search", "").strip()
    if search_query:
        jobs = jobs.filter(Q(title__icontains=search_query) | Q(company__name__icontains=search_query))

    paginator = Paginator(jobs, JOBS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "total_jobs": Job.objects.filter(is_approved=True, is_active=True).count(),
        "remote_count": Job.objects.filter(is_approved=True, is_active=True, is_remote=True).count(),
        "company_count": (Company.objects.filter(jobs__is_approved=True, jobs__is_active=True).distinct().count()),
    }
    return render(request, "jobs/index.html", context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_approved=True, is_active=True)
    related_jobs = (
        Job.objects.filter(company=job.company, is_approved=True, is_active=True)
        .exclude(pk=job.pk)
        .order_by("-created_at")[:3]
    )
    context = {
        "job": job,
        "related_jobs": related_jobs,
        "title": f"{job.title} at {job.company.name}",
        "description": job.short_description or f"{job.title} at {job.company.name}",
    }
    return render(request, "jobs/detail.html", context)


def companies(request):
    """Companies directory: companies with approved, active jobs."""
    company_qs = (
        Company.objects.filter(jobs__is_approved=True, jobs__is_active=True)
        .annotate(job_count=Count("jobs"))
        .order_by("name")
    )
    companies_list = []
    for company in company_qs:
        latest_jobs = Job.objects.filter(company=company, is_approved=True, is_active=True).order_by("-created_at")[:3]
        companies_list.append({"company": company, "job_count": company.job_count, "latest_jobs": latest_jobs})
    context = {
        "companies": companies_list,
        "title": "Companies",
        "description": "Companies hiring Python developers in the Philippines.",
    }
    return render(request, "jobs/companies.html", context)


@login_required
def post(request):
    job_posted = False
    company = request.user.companies.first()

    if request.method == "POST":
        company_form = CompanyForm(request.POST, instance=company)
        job_form = JobForm(request.POST)

        if company_form.is_valid() and job_form.is_valid():
            company = company_form.save(commit=False)
            company.user = request.user
            company.save()

            job = job_form.save(commit=False)
            job.user = request.user
            job.company = company
            job.save()
            job_posted = True
    else:
        company_form = CompanyForm(instance=company)
        job_form = JobForm()

    context = {
        "job_posted": job_posted,
        "company_form": company_form,
        "job_form": job_form,
    }
    return render(request, "jobs/post.html", context)
