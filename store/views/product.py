from rest_framework import viewsets
from store.models.product import Product, ProductVariant, Category
from store.serializers.product import ProductSerializer, ProductVariantSerializer, CategorySerializer
from rest_framework.permissions import AllowAny

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()

        group_slug = self.request.query_params.get("group_slug")
        if group_slug:
            queryset = queryset.filter(category__group_slug=group_slug)

        return queryset

class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    # def get_queryset(self):
    #     queryset = super().get_queryset()

    #     group_slug = self.request.query_params.get("group_slug")
    #     if group_slug:
    #         queryset = queryset.filter(group_slug=group_slug)

    #     return queryset
