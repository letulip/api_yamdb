from django.urls import path, include

from rest_framework import routers

from .views import UsersViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(
    r'users',
    UsersViewSet,
    basename='UsersViewSet'
)

urlpatterns = [
    path('', include(router.urls)),
]
