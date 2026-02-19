
import re
import os

backup_path = r'd:\django\oceania_gift_shop\shop\templates\shop\shop.html.backup'
target_path = r'd:\django\oceania_gift_shop\shop\templates\shop\shop.html'

if not os.path.exists(backup_path):
    print(f"Error: Backup file not found at {backup_path}")
    exit(1)

with open(backup_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix currency
content = content.replace('${{ product.price }}', '₹{{ product.price }}')

# Fix Category
content = re.sub(
    r'{% if selected_category==category\.id %}selected{% endif\s+%}>',
    r'{% if selected_category == category.id %}selected{% endif %}>',
    content
)

# Fix Sort - Price Low
# Using double quotes for the replacement string to avoid confusion with single quotes
content = re.sub(
    r'<option value="price_low" {% if sort_by==\'price_low\' %}selected{% endif %}>Price: Low to\s+High</option>',
    "<option value=\"price_low\" {% if sort_by == 'price_low' %}selected{% endif %}>Price: Low to High</option>",
    content
)

# Fix Sort - Price High
content = re.sub(
    r'<option value="price_high" {% if sort_by==\'price_high\' %}selected{% endif %}>Price: High to\s+Low</option>',
    "<option value=\"price_high\" {% if sort_by == 'price_high' %}selected{% endif %}>Price: High to Low</option>",
    content
)

# Fix Sort - Newest
content = content.replace(
    "{% if sort_by=='newest' %}",
    "{% if sort_by == 'newest' %}"
)

# Fix Sort - Name
content = content.replace(
    "{% if sort_by=='name' %}",
    "{% if sort_by == 'name' %}"
)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Overwrote shop.html with corrected content from backup.")
