
import os
import django
import sys

if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    sys.path.append("/home/Oceaniagifts/oceania_gift_shop")
else:
    sys.path.append(r"d:\django\oceania_gift_shop")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oceania_gift_shop.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import UserProfile, Category, Product, Coupon
from decimal import Decimal
import datetime
from django.utils import timezone

# Create Superuser
if not User.objects.filter(username='Admin').exists():
    u = User.objects.create_superuser('Admin', 'admin@example.com', 'password143')
    print("Superuser created: Admin/password143")
else:
    u = User.objects.get(username='Admin')

# Profile
if not hasattr(u, 'profile'):
    UserProfile.objects.create(user=u)
    print("Created profile for Admin")

# Categories
cats = ["Electronics", "Fashion", "Home & Living", "Toys & Games", "Books"]
cat_objs = {}
for c in cats:
    cat, created = Category.objects.get_or_create(name=c)
    cat_objs[c] = cat

# Products
if not Product.objects.exists():
    Product.objects.create(name="Smartphone X", description="Latest smartphone", price=Decimal("49999.00"), category=cat_objs["Electronics"], stock=10, featured=True)
    Product.objects.create(name="Headphones", description="Good sound", price=Decimal("2999.00"), category=cat_objs["Electronics"], stock=20)
    Product.objects.create(name="T-Shirt", description="Cotton", price=Decimal("499.00"), category=cat_objs["Fashion"], stock=50)
    print("Products created")

# Coupons
today = timezone.now()
expiry = today + datetime.timedelta(days=365)
if not Coupon.objects.filter(code="WELCOME").exists():
    Coupon.objects.create(code="WELCOME", discount=10, valid_from=today, valid_to=expiry, active=True)
if not Coupon.objects.filter(code="BIRTHDAY").exists():
    Coupon.objects.create(code="BIRTHDAY", discount=20, valid_from=today, valid_to=expiry, active=True)

print("Data seeded successfully.")
