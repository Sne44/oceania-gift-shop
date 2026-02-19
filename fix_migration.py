
import os
import django
from django.db import connection
import sys

sys.path.append(r"d:\django\oceania_gift_shop")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oceania_gift_shop.settings')
django.setup()

try:
    with connection.cursor() as cursor:
        print("Deleting 'shop' migrations from django_migrations table...")
        cursor.execute("DELETE FROM django_migrations WHERE app='shop'")
        print("Done.")
except Exception as e:
    print(f"Error: {e}")
