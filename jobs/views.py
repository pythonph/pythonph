from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import CompanyForm, JobForm


def index(request):
    context = dict(api_version='v1')
    return render(request, 'jobs/index.html', context)


@login_required
def post(request):
    job_posted = False
    company = request.user.companies.first()
    if request.method == 'POST':
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
    context = dict(job_posted=job_posted,
                   company_form=company_form,
                   job_form=job_form)
    return render(request, 'jobs/post.html', context)
