from rest_framework.routers import DefaultRouter
from store.views.product import ProductViewSet, ProductVariantViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'variants', ProductVariantViewSet, basename="variant")
router.register(r'categories', CategoryViewSet, basename="category")

urlpatterns = router.urls