"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from ecommerce_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('product/<int:product_id>/<slug:product_slug>/',
        views.show_product, name='product_detail'),
    path('cart/', views.show_cart, name='show_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('sale',views.sale,name='sale'), 
    path('signin',views.signin,name='signin'), 
    path('connected',views.connected,name='connected'), 
    path('connexion',views.connexion,name='connexion'),
    path('show_order',views.show_order,name='show_order'),
    path('show_sale',views.show_sale,name='show_sale'),  
    path('signout',views.signout,name='signout') ,
    re_path('^detail_order/(?P<order_id>[0-9]+)$', views.detail_order,name='detail_order'),
    re_path('^detail_sale/(?P<sale_id>[0-9]+)$', views.detail_sale,name='detail_sale'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
