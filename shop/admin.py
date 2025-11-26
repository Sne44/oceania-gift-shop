from django.contrib import admin
from .models import Product, Order, Payment




# Register Order Model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'product__name')

# Register Payment Model
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'paid', 'created_at')
    list_filter = ('paid',)
    search_fields = ('user__username', 'order__id')

from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to', 'active')
    search_fields = ('code',)
    list_filter = ('active', 'valid_from', 'valid_to')

from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'featured')  # ✅ Show featured in admin
    list_filter = ('featured',)  # ✅ Filter by featured

admin.site.register(Product, ProductAdmin)
