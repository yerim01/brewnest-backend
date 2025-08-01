from django.db import models
from django.contrib.auth import get_user_model
from store.models.product import ProductVariant

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)  # store Stripe payment intent ID
    shipping_address = models.TextField(blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Order #{self.id} by {self.user}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    
    # store prices directly in order, to preserve historical accuracy
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price_at_purchase

    def __str__(self):
        return f"{self.quantity} × {self.product_variant}"
    
    def to_order_item(self, order):
        return OrderItem(
            order=order,
            product_variant=self.product_variant,
            quantity=self.quantity,
            price_at_purchase=self.product_variant.final_price  # uses the `@property` in ProductVariant
        )
