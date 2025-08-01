from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Origin(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class RoastLevel(models.Model):
    level = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.level

class TastingNote(models.Model):
    tasting_note = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tasting_note

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=False, blank=False)
    origin = models.ForeignKey(Origin, on_delete=models.PROTECT, null=False, blank=False)
    roast_level = models.ForeignKey(RoastLevel, on_delete=models.SET_NULL, null=True, blank=True)
    tasting_note = models.ForeignKey(TastingNote, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    weight_grams = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.weight_grams}g"

    @property
    def final_price(self):
        return self.discount_price or self.price