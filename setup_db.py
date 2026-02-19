
import os
import shutil
import django
from django.core.management import call_command
import sys

# Add project root to sys.path
sys.path.append(r"d:\django\oceania_gift_shop")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oceania_gift_shop.settings')
django.setup()

# Clean up migrations
mig_dir = r"d:\django\oceania_gift_shop\shop\migrations"
if os.path.exists(mig_dir):
    for f in os.listdir(mig_dir):
        if f != "__init__.py" and f != "__pycache__":
            try:
                os.remove(os.path.join(mig_dir, f))
            except Exception as e:
                print(f"Error deleting {f}: {e}")

# Clean up DB
db_path = r"d:\django\oceania_gift_shop\db.sqlite3"
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("Deleted existing database.")
    except Exception as e:
        print(f"Error deleting database: {e}")

# Re-run migrations
print("Making migrations...")
call_command('makemigrations', 'shop')
print("Migrating...")
call_command('migrate')

# Create Superuser
from django.contrib.auth.models import User
print("Creating superuser...")
if not User.objects.filter(username='Admin').exists():
    u = User.objects.create_superuser('Admin', 'admin@example.com', 'password143')
    print("Superuser created: Admin/password143")
else:
    u = User.objects.get(username='Admin')

# Create UserProfile for Admin
from shop.models import UserProfile
if not hasattr(u, 'profile'):
    UserProfile.objects.create(user=u)
    print("Created profile for Admin")

# Create Categories
from shop.models import Category
cats = ["Electronics", "Fashion", "Home & Living", "Toys & Games", "Books"]
cat_objs = {}
for c in cats:
    cat, created = Category.objects.get_or_create(name=c)
    cat_objs[c] = cat
print("Created categories")

# Create Products
from shop.models import Product, Coupon
from decimal import Decimal
import datetime
from django.utils import timezone

if not Product.objects.exists():
    Product.objects.create(
        name="Smartphone X", 
        description="Latest smartphone with AI features", 
        price=Decimal("49999.00"), 
        category=cat_objs["Electronics"], 
        # image="products/smartphone.jpg", 
        stock=10, 
        featured=True
    )
    Product.objects.create(
        name="Wireless Headphones", 
        description="Active noise cancellation", 
        price=Decimal("2999.00"), 
        category=cat_objs["Electronics"], 
        stock=20
    )
    Product.objects.create(
        name="Cotton T-Shirt", 
        description="Comfortable daily wear", 
        price=Decimal("499.00"), 
        category=cat_objs["Fashion"], 
        stock=50
    )
    print("Created sample products")

# Create Coupons
today = timezone.now()
expiry = today + datetime.timedelta(days=365)
if not Coupon.objects.filter(code="WELCOME").exists():
    Coupon.objects.create(code="WELCOME", discount=10, valid_from=today, valid_to=expiry, active=True)
    print("Created WELCOME coupon")
if not Coupon.objects.filter(code="BIRTHDAY").exists():
    Coupon.objects.create(code="BIRTHDAY", discount=20, valid_from=today, valid_to=expiry, active=True)
    print("Created BIRTHDAY coupon")

print("Setup complete!")
