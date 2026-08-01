"""DRF router wiring for the Jobs API."""

from rest_framework.routers import DefaultRouter

from .api_views import CompanyViewSet, JobViewSet, UserViewSet

router = DefaultRouter()
router.register(r"user", UserViewSet)
router.register(r"company", CompanyViewSet)
router.register(r"job", JobViewSet)

urlpatterns = router.urls
