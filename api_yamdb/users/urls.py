from django.urls import path, include

from rest_framework import routers

from .views import UsersViewSet, UserAuthViewSet, UserKeyView, CurrentUserViewSet, CurrentUserDetailView

app_name = 'users'

router = routers.DefaultRouter()
# router.register(
#     r'users/me',
#     CurrentUserViewSet,
#     basename='CurrentUserViewSet'
# )
router.register(
    r'users',
    UsersViewSet,
    basename='UsersViewSet'
)
router.register(
    r'auth/signup',
    UserAuthViewSet,
    basename='UsersAuth'
)
# router.register(
#     r'auth/token',
#     UserKeyView,
#     basename='token_obtain_pair'
# )

urlpatterns = [
    path(
        'api/v1/users/me/',
        CurrentUserDetailView.as_view(),
        name='CurrentUserDetailView'
    ),
    path('api/v1/', include(router.urls)),
    path(
        'api/v1/auth/token/',
        UserKeyView.as_view(),
        name='token_obtain_pair'
    )
]
