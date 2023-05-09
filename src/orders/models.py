from django.db import models
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    stripe_checkout_session_id = models.CharField(max_length=220, null=True, blank=True)
    completed = models.BooleanField(default=False)
    strip_price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.username} - {self.completed}"
    