from django.contrib.auth import views
from django.urls import path

from .views import homepage, signup, profile, edit_profile, shop, about_shop, logout_page
from product_app.views import product_page

urlpatterns = [
    path('', homepage, name='homepage'),
    path('about_shop/', about_shop, name='about_shop'),
    path('logout_page/', logout_page, name="logout_page"),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='core_app/login.html'), name='login'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>/', product_page, name='product_page'),
]
