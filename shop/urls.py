from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import order_tracking

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('orders/', order_tracking, name='order_tracking'),
    path('membership/subscribe/', views.subscribe_membership, name='subscribe_membership'),
    path('membership/status/', views.membership_status, name='membership_status'),
    path('search/', views.search_products, name='search_products'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('fake-payment/<int:product_id>/', views.fake_payment, name='fake_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),  # ✅ Removed duplicate
    path('billing/<int:order_id>/', views.billing, name='billing'),
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'), 
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),


    path('order-summary/<int:order_id>/', views.order_summary, name='order_summary'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
