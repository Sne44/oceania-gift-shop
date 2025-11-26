from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from .models import Product, Order, Payment, Coupon, Membership, Wishlist, Review, Category
from .forms import ReviewForm

# Home Page
def home(request):
    featured_products = Product.objects.filter(featured=True)[:6]
    new_arrivals = Product.objects.order_by("-id")[:6]
    categories = Category.objects.all()
    
    # Get user orders only if the user is logged in
    orders = Order.objects.filter(user=request.user).order_by('-created_at') if request.user.is_authenticated else None
    
    return render(request, "shop/home.html", {
        "featured_products": featured_products,
        "new_arrivals": new_arrivals,
        "categories": categories,
        "orders": orders,  # Pass orders to the template
    })
# Shop View
def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "shop/shop.html", {"products": products, "categories": categories})

# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_detail.html", {"product": product})

# Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(
        user=request.user, product=product, status="Pending",
        defaults={'quantity': 1, 'total_price': product.price}
    )
    if not created:
        order.quantity += 1
        order.total_price = order.quantity * product.price
        order.save()

    return redirect("cart")

# View Cart
@login_required
def cart(request):
    orders = Order.objects.filter(user=request.user, status="Pending")
    total_amount = sum(order.total_price for order in orders)
    return render(request, "shop/cart.html", {"orders": orders, "total_amount": total_amount})

# Remove from Cart
@login_required
def remove_from_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status="Pending")
    order.delete()
    return redirect("cart")

# Checkout View



# Fake Payment (For Testing)
@login_required
def fake_payment(request):
    orders = Order.objects.filter(user=request.user, status="Pending")

    if request.method == "POST":
        shipping_address = request.POST.get("address", "").strip()
        card_number = request.POST.get("card_number", "").strip()
        expiry_date = request.POST.get("expiry_date", "").strip()
        cvv = request.POST.get("cvv", "").strip()

        if len(card_number) == 16 and len(cvv) == 3:
            for order in orders:
                order.status = "Paid"
                order.shipping_address = shipping_address
                order.save()

                Payment.objects.create(
                    user=request.user,
                    order=order,
                    amount=order.total_price,
                    paid=True
                )

            messages.success(request, "Payment successful! Your order is confirmed.")
            return redirect("payment_success")

        else:
            messages.error(request, "Invalid payment details! Try again.")
            return redirect("checkout")

    return render(request, "shop/fake_payment.html", {"orders": orders})

# Payment Success Page
def payment_success(request):
    return render(request, "shop/payment_success.html")

# Order Tracking
@login_required
def order_tracking(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "shop/order_tracking.html", {"orders": orders})

# Add to Wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.create(user=request.user, product=product)
    return redirect("wishlist")

# View Wishlist
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, "shop/wishlist.html", {"wishlist_items": wishlist_items})

# Remove from Wishlist
@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    return redirect("wishlist")

# Add Review
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect("product_detail", product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, "shop/add_review.html", {"form": form, "product": product})

# Membership Subscription
@login_required
def subscribe_membership(request):
    if not hasattr(request.user, 'membership'):
        Membership.objects.create(user=request.user, is_member=True, discount_percentage=10)
        messages.success(request, "You are now a premium member with a 10% discount.")
    else:
        messages.info(request, "You are already a premium member.")

    return redirect("membership_status")

# Membership Status
@login_required
def membership_status(request):
    membership = getattr(request.user, 'membership', None)
    return render(request, "shop/membership_status.html", {"membership": membership})

# User Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

# User Login
def login_view(request):
    return render(request, 'shop/login.html')
def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'shop/search_results.html', {'products': products})

def shop_view(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})
def billing(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'shop/billing.html', {'order': order})

def payment_cancel(request):
    return render(request, 'shop/payment_cancel.html')
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Product

def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/checkout.html', {'product': product})
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404

def fake_payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address")
        amount_paid = product.price  # Get product price

        return render(request, "shop/payment_success.html", {
            "product": product,
            "amount_paid": amount_paid,  # Pass amount to template
            "shipping_address": shipping_address,
        })

    return render(request, "shop/fake_payment.html", {"product": product})
@login_required
def order_tracking(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_tracking.html', {'orders': orders})

from .models import Product, Review
from .forms import ReviewForm

from .models import Product, Review
from .forms import ReviewForm

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect("product_detail", product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, "shop/product_detail.html", {"product": product, "form": form})
from django.shortcuts import render, get_object_or_404
from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "shop/order_summary.html", {"order": order})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Coupon

def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    coupons = Coupon.objects.all()  # Fetch available coupons

    applied_coupon = None
    discount_amount = 0
    final_amount = product.price

    if request.method == 'POST':
        if 'coupon_code' in request.POST:  # If a coupon is applied
            coupon_code = request.POST.get('coupon_code')
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                applied_coupon = coupon_code
                discount_amount = (product.price * coupon.discount) / 100
                final_amount = product.price - discount_amount
                messages.success(request, f"Coupon {coupon_code} applied! Discount: ₹{discount_amount}")
            except Coupon.DoesNotExist:
                messages.error(request, "Invalid coupon code")

        elif 'pay_now' in request.POST:  # If "Proceed to Payment" is clicked
            # Redirect to fake payment page
            return redirect('fake_payment', product_id=product.id)  

    context = {
        'product': product,
        'coupons': coupons,
        'applied_coupon': applied_coupon,
        'discount_amount': discount_amount,
        'final_amount': final_amount
    }
    return render(request, 'shop/checkout.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Address
from .forms import AddressForm

@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.save()
            return redirect('manage_addresses')
    else:
        form = AddressForm()
    return render(request, 'shop/add_address.html', {'form': form})
@login_required
def manage_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'shop/manage_addresses.html', {'addresses': addresses})
