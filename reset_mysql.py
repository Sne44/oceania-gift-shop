
import os
import django
import sys
from django.db import connection

sys.path.append(r"d:\django\oceania_gift_shop")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oceania_gift_shop.settings')
django.setup()

try:
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if not tables:
            print("No tables found to drop.")
        else:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            for table in tables:
                t_name = table[0]
                print(f"Dropping table {t_name}")
                cursor.execute(f"DROP TABLE IF EXISTS {t_name}")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    print("All tables dropped successfully.")
except Exception as e:
    print(f"Error dropping tables: {e}")
