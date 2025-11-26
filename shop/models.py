from django.db import models
from django.contrib.auth.models import User

# Product Model

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0) 
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    wishlist = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Order Model



from django.db import models
from django.contrib.auth.models import User
from .models import Product  # Ensure Product model is imported
import uuid



import uuid
from django.db import models
from django.contrib.auth.models import User

ORDER_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
]

PAYMENT_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Paid", "Paid"),
    ("Failed", "Failed"),
]

class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default="Pending")
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="Pending")
    shipping_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Unpaid", "Unpaid")], default="Unpaid")  
    delivered_at = models.DateTimeField(blank=True, null=True)
    order_number = models.CharField(max_length=20, unique=True, null=True, blank=True)  # ✅ Ensure this field exist

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"

    def save(self, *args, **kwargs):
        """Auto-calculate total price before saving"""
        if self.product:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def get_total_price(self):
        """Returns the total price of the order"""
        return self.product.price * self.quantity if self.product else 0


# Payment Model
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username}"

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage (e.g., 10 for 10%)")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.discount}%"
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}⭐"
class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_member = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)

    def __str__(self):
        return f"{self.user.username} - Member"
class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")  # ✅ Fix conflict

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Your custom fields here (if any)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Avoids conflict with Django’s default User model
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Avoids conflict
        blank=True,
    )

    def __str__(self):
        return self.username
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.IntegerField()  # Discount percentage
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"{self.code} - {self.discount}% Off"
    from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name}, {self.street_address}, {self.city}, {self.state}"

    class Meta:
        verbose_name_plural = "Addresses"
