from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from product_app.models import Product, Category

from .forms import SignUpForm


def homepage(request):
    products = Product.objects.all()[0:8]
    return render(request, 'core_app/homepage.html', {'products': products})


def about_shop(request):
    return render(request, 'core_app/about_shop.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")


def signup(request):
    """
    New user registration page
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, "core_app/signup.html", {'form': form})


@login_required
def profile(request):
    """
    User's personal account page
    """
    return render(request, 'core_app/profile.html')


@login_required
def edit_profile(request):
    """
    Account edit page
    """
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()

        return redirect('profile')
    return render(request, 'core_app/edit_profile.html')


def shop(request):
    """
    Store gallery page with catalog and search bar
    """
    categories = Category.objects.all()
    products = Product.objects.all()
    active_category = request.GET.get('category')
    if active_category:
        products = products.filter(category__slug=active_category)
    query = request.GET.get('query')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category,
    }

    return render(request, 'core_app/shop.html', context)
