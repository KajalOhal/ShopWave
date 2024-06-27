from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileForm, AddressForm
from .models import Profile,Product, Category, Order, OrderItem, Cart, CartItem, Brand, Address
from django.contrib import messages
from django.db.models import Q

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'ecommerce_app/user_profile.html', {'form': form})

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    distinct_brands = Brand.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category__id=category_id)

    query = request.GET.get('query')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )


    context = {
        'categories': categories,
        'products': products,
        'distinct_brands': distinct_brands,
    }
    return render(request, 'ecommerce_app/home.html', context)

def products_by_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    products = Product.objects.filter(brand=brand)
    context = {
        'products': products,
        'brand': brand
    }
    return render(request, 'ecommerce_app/products_by_brand.html', context)


def product_detail_id(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product,
    }
    return render(request, 'ecommerce_app/product_detail.html', context)

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    addresses = Address.objects.filter(user=request.user)
    context = {
        'product': product,
        'addresses': addresses
    }
    return render(request, 'ecommerce_app/buy_now.html', context)

def search(request):
    query = request.GET.get('query')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Item added to cart successfully.')
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'ecommerce_app/cart.html', {'cart_items': cart_items})


@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        cart_item.quantity = int(quantity)
        cart_item.save()
        return redirect('view_cart')
    return render(request, 'ecommerce_app/update_cart.html', {'cart_item': cart_item})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment_option = request.POST.get('payment')
       
        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirmation')  # Redirect to order confirmation page
    else:
        return redirect('home')
    
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'ecommerce_app/order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'ecommerce_app/order_history.html', {'orders': orders})



