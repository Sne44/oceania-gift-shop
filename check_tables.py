
import os
import django
from django.db import connection
import sys

sys.path.append(r"d:\django\oceania_gift_shop")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oceania_gift_shop.settings')
django.setup()

try:
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        print("Tables in DB:", tables)
except Exception as e:
    print(e)
