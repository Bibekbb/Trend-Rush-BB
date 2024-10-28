from django.shortcuts import render, redirect, HttpResponse
from app.models import Category, SubCategory, Product, Contact_us, Order, Brand, CartItem, UserInteraction
from django.contrib.auth import authenticate, login
from app.forms import UserCreationForm
from django.core.paginator import Paginator

from app.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
from datetime import datetime
# from app.utils import get_item_recommendations
from django.contrib.sessions.backends.db import SessionStore
from app.product_recommended import get_item_recommend
# from app.prod_recomm import get_item_recommendations
from app.recommed import get_item_recommendations


def base(request):
    now = datetime.now()
    context = {
        'current_date': now.date(),
        'current_time': now.time(),
    }
    return render(request, 'base.html', context)


def index(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')

    product_queryset = Product.objects.filter(
        Avaliability='In Stock').order_by('-id')

    if category_id:
        product_queryset = product_queryset.filter(
            subcategory=category_id).order_by('-id')
    elif brand_id:
        product_queryset = product_queryset.filter(
            brand=brand_id).order_by('-id')

    paginator = Paginator(product_queryset, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    recommended_page = paginator.get_page(page_number)

    if 'cart' in request.session:
        cart = request.session['cart']
        recommended_products = get_item_recommendations(
            cart, num_recommendations=5)
    else:
        recommended_products = []

    min_price = 0
    max_price = 600

    context = {
        'category': category,
        'brand': brand,
        'min_price': min_price,
        'max_price': max_price,
        'recommended_products': recommended_products,
        'recommended_products': recommended_page,
        'page': page,
    }
    return render(request, 'index.html', context)

def Recommendations(request):
    # Check if 'cart' is in the session
    if 'cart' in request.session:
        cart = request.session['cart']
        recommended_products = get_item_recommendations(
            cart, num_recommendations=5)
    else:
        recommended_products = []

    context = {
        'recommended_products': recommended_products,
    }

    return render(request, 'recommended.html', context)

def Product_Page(request):
    category = Category.objects.all().order_by('-id')
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')

    if categoryID:
        product = Product.objects.filter(
            subcategory=categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all().order_by('-id')

    context = {
        'category': category,
        'brand': brand,
        'product': product,
    }
    return render(request, 'product.html', context)


# For Signup
def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def contact_page(request):
    if request.method == 'POST':
        contact = Contact_us(
            name=request.post.get('name'),
            email=request.post.get('email'),
            subject=request.post.get('subject'),
            message=request.post.get('message'),
        )
        contact.save()

    return render(request, 'contact/contact.html')


def CheckOut(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        zipcode = request.POST.get('zipcode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)
        print(cart)
        for i in cart:
            a = cart[i]['price']
            b = cart[i]['quantity']
            total = a*b
            order = Order(
                user=user,
                product=cart[i]['name'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                phone=phone,
                zipcode=zipcode,
                total=total,
            )
            order.save()
        request.session['cart'] = {}
        return redirect('index')

    return HttpResponse("This is the checkout Page")


def YourOrder(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order = Order.objects.filter(user=user)
    context = {
        'order': order
    }
    return render(request, 'order.html', context)


def Product_Detail(request, id):
    product = Product.objects.filter(id=id).first()
    review = Product.objects.count()
    category = Category.objects.all()
    brand = Brand.objects.all()
    subcat = SubCategory.objects.all()

    if 'cart' in request.session:
        cart = request.session['cart']
        recommended_products = get_item_recommend(
            cart, num_recommendations=5)
    else:
        recommended_products = []

    context = {
        'category': category,
        'product': product,
        'review': review,
        'brand': brand,
        'subcat': subcat,
        'recommended_products': recommended_products,

    }

    return render(request, 'product_detail.html', context)


def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains=query)
    context = {
        'product': product,
    }
    return render(request, 'search.html', context)
