from django.contrib.auth.models import User
from jobs.models import Company, Job
from tastypie.constants import ALL
from tastypie import fields
from tastypie.api import Api
from tastypie.resources import ModelResource


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name']

    def dehydrate(self, bundle):
        bundle.data['name'] = bundle.obj.get_full_name()
        return bundle


class CompanyResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Company.objects.all()

    def obj_create(self, bundle, **kwargs):
        return super(CompanyResource, self).obj_create(
            bundle,
            user=bundle.request.user,
        )


class JobResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    company = fields.ForeignKey(CompanyResource, 'company', full=True)
    # TODO: Include tags

    class Meta:
        queryset = Job.objects.all()
        filtering = {
            'is_approved': ALL,
            'is_sponsored': ALL,
        }

    def build_filters(self, filters=None):
        filters = {} if filters is None else filters
        filters.setdefault('is_approved', True)
        return super(JobResource, self).build_filters(filters)

    def apply_sorting(self, obj_list, options=None):
        return obj_list.order_by('is_sponsored', '-updated_at')

    def obj_create(self, bundle, **kwargs):
        return super(JobResource, self).obj_create(
            bundle,
            user=bundle.request.user,
        )


v1 = Api(api_name='v1')
v1.register(UserResource())
v1.register(CompanyResource())
v1.register(JobResource())

