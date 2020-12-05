from django.urls import path
from . import views
from store.auth import auth_middleware

urlpatterns = [
    path('',views.index),
    path('signup',views.signup),
    path('login',views.login,name='login'),
    path('logout',views.logout),
    path('cart',views.cart,name='cart'),
    path('check-out',views.checkout),
    path('orders',auth_middleware(views.orderss)),
    path('about',views.about),
    path('contact',views.contact)
] 

