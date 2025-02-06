from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import (SignUpViewSet, SignInViewSet,
                    ProfileViewSet, CollectionViewSet,
                    ProductViewSet, ProductImageViewSet,
                    CustomerViewSet, CartViewSet,
                    CartItemViewSet)


router = DefaultRouter()
router.register("signup", SignUpViewSet, basename="sign-up")
router.register("signin", SignInViewSet, basename="sign-in")
router.register("profile", ProfileViewSet, basename="profile")
router.register('collections', viewset=CollectionViewSet, basename='collection')
router.register('products', viewset=ProductViewSet, basename='product')
router.register('customers', viewset=CustomerViewSet, basename='customer')
router.register('carts', viewset=CartViewSet, basename='cart')

products_router = NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('images', viewset=ProductImageViewSet, basename='product-image')

carts_router = NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', viewset=CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls)),
]