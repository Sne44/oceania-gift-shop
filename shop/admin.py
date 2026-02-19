
from django.contrib import admin
from .models import Product, Order, Payment, Category, Coupon, Membership, Wishlist, Review, Address, UserProfile, CouponUsage

# Customize Admin Site Header
admin.site.site_header = "Oceania Gift Shop Admin"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'featured')
    list_filter = ('category', 'featured')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'product', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username')

admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Membership)
admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(Address)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active', 'valid_from', 'valid_to')
    list_filter = ('active',)
    search_fields = ('code',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birthday')

@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'used_at')
