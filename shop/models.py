
from django.db import models
from django.contrib.auth.models import User
import uuid

# Categories
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self): return self.name

# Products
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    wishlist = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    def __str__(self): return self.name

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField(null=True, blank=True)
    def __str__(self): return f"Profile: {self.user.username}"

# Orders
class Order(models.Model):
    ORDER_STATUS = [("Pending","Pending"), ("Shipped","Shipped"), ("Delivered","Delivered"), ("Cancelled","Cancelled")]
    PAYMENT_STATUS = [("Pending","Pending"), ("Paid","Paid"), ("Failed","Failed")]
    
    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="Pending")
    shipping_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.product:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self): return f"Order {str(self.order_number)[:8]}"

# Payments
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Payment {self.id}"

# Coupons
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.IntegerField(help_text="Discount percentage (e.g., 10 for 10%)")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    def __str__(self): return f"{self.code} ({self.discount}%)"

# Coupon Usage
class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user.username} - {self.coupon.code}"

# Membership
class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_member = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)

# Wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")

# Review
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Address
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
    class Meta: verbose_name_plural = "Addresses"
