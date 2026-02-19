
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login
from django.db.models import Sum

from .models import Product, Order, Payment, Coupon, Membership, Wishlist, Review, Category, UserProfile, CouponUsage, Address
from .forms import ReviewForm, UserRegisterForm, AddressForm

# Home
def home(request):
    featured_products = Product.objects.filter(featured=True)[:6]
    categories = Category.objects.all()
    # If user is authenticated, otherwise None
    orders = Order.objects.filter(user=request.user).order_by('-created_at') if request.user.is_authenticated else None
    return render(request, "shop/home.html", {"orders": orders, "featured_products": featured_products, "categories": categories})

# Shop Filtering
def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort')

    if category_id:
        try: category_id = int(category_id)
        except ValueError: category_id = None
        if category_id: products = products.filter(category_id=category_id)

    if min_price:
        try: products = products.filter(price__gte=float(min_price))
        except ValueError: pass
    if max_price:
        try: products = products.filter(price__lte=float(max_price))
        except ValueError: pass
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    if sort_by == 'price_low': products = products.order_by('price')
    elif sort_by == 'price_high': products = products.order_by('-price')
    elif sort_by == 'newest': products = products.order_by('-created_at')
    elif sort_by == 'name': products = products.order_by('name')

    return render(request, "shop/shop.html", {
        "products": products, "categories": categories,
        "selected_category": category_id,
        "min_price": min_price, "max_price": max_price,
        "search_query": search_query, "sort_by": sort_by
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_detail.html", {"product": product})

@login_required
def add_to_cart(request, product_id):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admins are not allowed to purchase items.")
        return redirect('home')

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

@login_required
def cart(request):
    orders = Order.objects.filter(user=request.user, status="Pending")
    total_amount = sum(order.total_price for order in orders)
    return render(request, "shop/cart.html", {"orders": orders, "total_amount": total_amount})

@login_required
def remove_from_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status="Pending")
    order.delete()
    return redirect("cart")

@login_required
def decrease_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status="Pending")
    if order.quantity > 1:
        order.quantity -= 1
        order.total_price = order.quantity * order.product.price
        order.save()
    else:
        order.delete()
    return redirect("cart")

def validate_coupon_logic(user, coupon):
    # Welcome
    if coupon.code == "WELCOME":
        if CouponUsage.objects.filter(user=user, coupon=coupon).exists():
            return False, "Welcome coupon can only be used once."
    # Birthday
    elif coupon.code == "BIRTHDAY":
        today = timezone.now().date()
        if CouponUsage.objects.filter(user=user, coupon=coupon, used_at__year=today.year).exists():
            return False, "Birthday coupon used already this year."
        
        try:
            # Safely access profile
            if hasattr(user, 'profile'):
                profile = user.profile
                if not profile.birthday:
                    return False, "No birthday set in profile."
                if (profile.birthday.month != today.month) or (profile.birthday.day != today.day):
                    return False, "Birthday coupon is only valid on your birthday."
            else:
                return False, "UserProfile not found."
        except UserProfile.DoesNotExist:
            return False, "UserProfile not found."
    return True, None

@login_required
def checkout(request, product_id):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admins are not allowed to purchase items.")
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    coupons = Coupon.objects.filter(active=True)
    
    final_amount = product.price
    discount_amount = 0
    applied_coupon_code = None

    if request.method == "POST":
        if "pay_now" in request.POST:
             return redirect('fake_payment', product_id=product.id)
        
        # Coupon Logic
        coupon_code = request.POST.get("coupon_code")
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                valid, error = validate_coupon_logic(request.user, coupon)
                
                if not valid:
                    messages.error(request, error)
                else:
                    discount_val = (product.price * coupon.discount) / 100
                    discount_amount = round(discount_val, 2)
                    final_amount = product.price - discount_amount
                    applied_coupon_code = coupon.code
                    
                    # Save to session
                    request.session['coupon_code'] = coupon.code
                    request.session['coupon_product_id'] = product.id
                    
                    messages.success(request, f"Coupon applied! You saved ₹{discount_amount}")

            except Coupon.DoesNotExist:
                messages.error(request, "Invalid coupon code.")

    # Retrieve from session if exists and matches
    elif request.method == "GET":
        sess_code = request.session.get('coupon_code')
        sess_pid = request.session.get('coupon_product_id')
        if sess_code and sess_pid == product.id:
            try:
                coupon = Coupon.objects.get(code=sess_code, active=True)
                valid, _ = validate_coupon_logic(request.user, coupon)
                if valid:
                    discount_val = (product.price * coupon.discount) / 100
                    discount_amount = round(discount_val, 2)
                    final_amount = product.price - discount_amount
                    applied_coupon_code = coupon.code
            except Coupon.DoesNotExist:
                pass

    return render(request, 'shop/checkout.html', {
        'product': product,
        'coupons': coupons,
        'discount_amount': discount_amount,
        'final_amount': final_amount,
        'applied_coupon': applied_coupon_code
    })

@login_required
def fake_payment(request, product_id):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admins are not allowed to purchase items.")
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    
    amount_paid = product.price
    coupon_code = request.session.get('coupon_code')
    sess_pid = request.session.get('coupon_product_id')
    used_coupon = None

    if coupon_code and sess_pid == product.id:
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            valid, _ = validate_coupon_logic(request.user, coupon)
            if valid:
                discount_val = (product.price * coupon.discount) / 100
                amount_paid = product.price - round(discount_val, 2)
                used_coupon = coupon
        except Coupon.DoesNotExist:
            pass

    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address")

        # Create Order
        order = Order.objects.create(
            user=request.user, product=product, quantity=1,
            shipping_address=shipping_address, status="Pending", payment_status="Paid"
        )
        # Create Payment
        Payment.objects.create(user=request.user, order=order, amount=amount_paid, paid=True)
        
        # Record Usage
        if used_coupon:
            CouponUsage.objects.create(user=request.user, coupon=used_coupon)
            # Clear session
            if 'coupon_code' in request.session: del request.session['coupon_code']
            if 'coupon_product_id' in request.session: del request.session['coupon_product_id']
            
        return render(request, "shop/payment_success.html", {
            "product": product,
            "amount_paid": amount_paid,
            "shipping_address": shipping_address,
        })

    return render(request, "shop/fake_payment.html", {"product": product, "amount_to_pay": amount_paid})

@login_required
def order_tracking(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "shop/order_tracking.html", {"orders": orders})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.create(user=request.user, product=product)
    return redirect("wishlist")

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, "shop/wishlist.html", {"wishlist_items": wishlist_items})

@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    return redirect("wishlist")

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

@login_required
def subscribe_membership(request):
    if not hasattr(request.user, 'membership'):
        Membership.objects.create(user=request.user, is_member=True, discount_percentage=10)
        messages.success(request, "You are now a premium member with a 10% discount.")
    else:
        messages.info(request, "You are already a premium member.")
    return redirect("membership_status")

@login_required
def membership_status(request):
    membership = getattr(request.user, 'membership', None)
    return render(request, "shop/membership_status.html", {"membership": membership})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    return render(request, 'shop/login.html')

def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'shop/search_results.html', {'products': products})

@login_required
def billing(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/billing.html', {'order': order})

def payment_cancel(request):
    return render(request, 'shop/payment_cancel.html')

def payment_success(request):
    return render(request, 'shop/payment_success.html')

@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "shop/order_summary.html", {"order": order})

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
