from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter
from .views import SignUpViewSet, SignInViewSet, ProfileViewSet


router = DefaultRouter()
router.register("signup", SignUpViewSet, basename="sign-up")
router.register("signin", SignInViewSet, basename="sign-in")
router.register("profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
]