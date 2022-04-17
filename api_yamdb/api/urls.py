from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ReviewViewSet, CommentViewSet

app_name = 'api'

router = SimpleRouter()
# Поправить урл согласно документации
router.register('reviews', ReviewViewSet)
router.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
