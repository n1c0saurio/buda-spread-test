from rest_framework.routers import DefaultRouter
from .views import SpreadViewSet

router = DefaultRouter()
router.register(r"spreads", SpreadViewSet, basename="spread")
urlpatterns = router.urls
