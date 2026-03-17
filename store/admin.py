from django.contrib import admin

from store.models.product import Category, Origin, RoastLevel, TastingNote, Product, ProductVariant

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'origin', 'is_active')
    inlines = [ProductVariantInline]