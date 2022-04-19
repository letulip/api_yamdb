from django.urls import path, include

from rest_framework import routers

from .views import (
    UsersViewSet,
    UserKeyView,
    UserAuthView
)

app_name = 'users'

router = routers.DefaultRouter()
router.register(
    r'users',
    UsersViewSet,
    basename='UsersViewSet'
)

urlpatterns = [
    path(
        'api/v1/auth/signup/',
        UserAuthView.as_view(),
        name='register_user'
    ),
    path(
        'api/v1/auth/token/',
        UserKeyView.as_view(),
        name='token_obtain_pair'
    ),
    path('api/v1/', include(router.urls)),
]
