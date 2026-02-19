
import os
import django
from django.db import connection
import sys

sys.path.append(r"d:\django\oceania_gift_shop")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oceania_gift_shop.settings')
django.setup()

try:
    with connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        # List all shop tables based on models
        tables = [
            "shop_category", 
            "shop_product", 
            "shop_order", 
            "shop_payment", 
            "shop_coupon", 
            "shop_membership", 
            "shop_wishlist", 
            "shop_review", 
            "shop_address", 
            "shop_userprofile", 
            "shop_couponusage"
        ]
        for t in tables:
            print(f"Dropping {t}...")
            cursor.execute(f"DROP TABLE IF EXISTS {t}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    print("Shop tables dropped.")
except Exception as e:
    print(f"Error: {e}")
