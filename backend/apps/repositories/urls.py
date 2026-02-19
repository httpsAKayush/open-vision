from rest_framework.routers import DefaultRouter
from .views import RepositoryViewSet

router = DefaultRouter()
router.register('', RepositoryViewSet)
urlpatterns = router.urls
