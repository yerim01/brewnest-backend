from rest_framework import serializers
from store.models.product import Category, Origin, RoastLevel, TastingNote, Product, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = ['id', 'name']

class RoastLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoastLevel
        fields = ['id', 'level']

class TastingNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TastingNote
        fields = ['id', 'tasting_note']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'weight_grams', 'price', 'discount_price', 'stock', 'final_price']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    origin = OriginSerializer()
    roast_level = RoastLevelSerializer()
    tasting_note = TastingNoteSerializer()
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'origin', 'roast_level', 'tasting_note',
            'description', 'image', 'is_active', 'created_at', 'variants'
        ]
