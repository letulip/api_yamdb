from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    ReviewSingleView,
    CommentViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews'
# )
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path(
        'api/v1/titles/<int:title_id>/reviews/',
        ReviewViewSet.as_view(),
        name='reviews'
    ),
    path(
        'api/v1/titles/<int:title_id>/reviews/<int:review_id>/',
        ReviewSingleView.as_view(),
        name='review'
    )
]
