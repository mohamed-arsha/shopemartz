"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('shop/',views.shop,name='shop'),
    path('shop/catfilter/<int:id>/',views.catfilter,name='catfilter'),
    path('shop/shopdetail/<int:id>/',views.shop_detail,name='shopdetail'),
    path('shop/shopdetail/cart/<int:id>',views.cart,name='cart'),
    path('shop/shopdetail/cart/view_cart',views.view_cart,name='view_cart'),
    path('shop/shopdetail/cart/add/view_cart/decrement/<str:id>',views.decreament,name='cart_dec'),
    path('shop/shopdetail/cart/add/view_cart/increment/<str:id>',views.increment,name='cart_inc'),
    path('shop/shopdetail/cart/add/view_cart/one_item/delete/<str:id>',views.deletecartoneitem,name='deletecartoneitem'),
    path('shop/shopdetail/cart/delete_cart',views.clearcarts,name='clearcarts'),
    path('shop/shopdetail/cart/checkout',views.checkout,name='checkout'),
    path('shop/shopdetail/cart/billingdetails',views.billing_details,name='billing_details'),
    path('shop/shopdetail/cart/cashondelivery',views.codordersuccessfully,name='codordersuccessfully'),
    path('login/myorder',views.myorder,name='myorder'),
    path('category',views.category,name='category'),
    path('newarrivals',views.newarrivals,name='newarrivals'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

