from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    APIReviewDetail,
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
    'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path(
        'titles/<int:title_id>/reviews/',
        ReviewViewSet.as_view(),
        name='reviews'
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/',
        APIReviewDetail.as_view(),
        name='review_detail'
    ),
    path('', include(router.urls)),
]
