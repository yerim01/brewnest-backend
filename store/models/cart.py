from django.db import models
from django.contrib.auth import get_user_model
# from store.models.product import ProductVariant

User = get_user_model()

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product_variant = models.ForeignKey("store.ProductVariant", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_variant')  # ensures no duplicates for the same variant

    def __str__(self):
        return f"{self.quantity} × {self.product_variant} (User: {self.user})"

    def get_total_price(self):
        return self.quantity * getattr(self.product_variant, 'final_price', self.product_variant.price)
