from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings




class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    # Add any additional fields you want to include in your custom user model
    # For example:
    # bio = models.TextField(blank=True)
    pass


# Create your models here.

class Product(models.Model):
    """
    Model representing a product.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def is_in_stock(self):
        """
        Check if the product is in stock.
        """
        return self.stock > 0

    def __str__(self):
        return self.name
    
class Order(models.Model):
    """
    Model representing an order
    """
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        DELIVERED = 'Delivered', 'Delivered'
        CANCELLED = 'Cancelled', 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders', blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    """
    Model representing an item in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        """
        Calculate the total price for this order item.
        """
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"
