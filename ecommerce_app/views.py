from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Order, LineItem,Categories,LineItemSale,Sale,Table
from .forms import CartForm, CheckoutForm,signinForm,SaleForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
from . import cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
import datetime
import os
from twilio.rest import Client



def is_valid_queryparam(param):
    return param!='' and param is not None
# Create your views here.

def connected(request):
    
    return render(request,'compte/connected.html') 

def connexion(request):
    
    return render(request,'compte/connexion.html') 


def detail_order(request,order_id):
    detail_order=LineItem.objects.filter(order_id=order_id)
    return render(request,'ecommerce_app/detail_order.html',{'detail_order':detail_order})

def detail_sale(request,sale_id):
    detail_sale=LineItemSale.objects.filter(sale_id=sale_id)
    return render(request,'ecommerce_app/detail_sale.html',{'detail_sale':detail_sale})



def index(request):
    all_products = Product.objects.filter(available=True).order_by('name')
    all_categorie = Categories.objects.all().order_by('categories')
    categorie=request.POST.get('categorie_id') 
    context={}
    if request.method == 'POST':
        all_products = Product.objects.filter(categorie_id=categorie,available=True).order_by('name')
        context['all_products']=all_products              
        context['all_categorie']=all_categorie   
        return render(request, "ecommerce_app/index.html",context)
    paginator=Paginator(all_products,30)
    page=request.GET.get('page')
    try:
        all_products=paginator.page(page)
    except PageNotAnInteger:
        all_products=paginator.page(1)
    except EmptyPage:
        all_products=paginator.page(paginator.num_pages)  
    context['paginate']=True 
    context['all_products']=all_products              
    context['all_categorie']=all_categorie   
    return render(request, "ecommerce_app/index.html",context)

def show_product(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CartForm(request, request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect('show_cart')

    form = CartForm(request, initial={'product_id': product.id})
    return render(request, 'ecommerce_app/product_detail.html', {
                                            'product': product,
                                            'form': form,
                                            })

def show_cart(request):

    if request.method == 'POST':
        if request.POST.get('submit') == '+':
            cart.plus_item(request)
        if request.POST.get('submit') == '-':
            cart.moins_item(request)    
        if request.POST.get('submit') == 'X':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    cart_subtotal = cart.subtotal(request)
    return render(request, 'ecommerce_app/cart.html', {
                                            'cart_items': cart_items,
                                            'cart_subtotal': cart_subtotal,
                                            })


def show_order(request):
    aujourdhui =datetime.date.today()
    if request.method == 'POST':
        if request.POST.get('submit') == 'encours':
            cart.order_encours_item(request)
        if request.POST.get('submit') == 'servir':
            cart.order_servir_item(request)    
    order_items = Order.objects.filter(date_addedunique=aujourdhui)
    return render(request, 'ecommerce_app/show_order.html', {
                                            'order_items': order_items,
                                            'aujourdhui': aujourdhui,
                                            })


def checkout(request):
    cart_subtotal = cart.subtotal(request)
    tablet=Table.objects.all().order_by('table')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            o = Order(
                Table = cleaned_data.get('Table'),
                Total = cleaned_data.get('Total'),   
            )
            o.save()

            tablenumero=cleaned_data.get('Table')
            num=get_object_or_404(Table,table=tablenumero)
            account_sid = "AC1bb1ed2d2fddbeb262ac0c0bc7ad034a"
            auth_token = "9a00e6ca297dabdb75afd918b802eadc"
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body="Vous avez une commande encours sur la table" + " " + num.table,
            from_="+14345055769",
            to=num.numero
            )
            print(message.sid)

            all_items = cart.get_all_cart_items(request)
            for cart_item in all_items:
                li = LineItem(
                    product_id = cart_item.product_id,
                    price = cart_item.price,
                    quantity = cart_item.quantity,
                    order_id = o.id
                )
                li.save()
            cart.clear(request)
            request.session['order_id'] = o.id
            messages.add_message(request, messages.INFO, 'Commande envoyée avec success!')
            return redirect('checkout')
    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', {'form': form,
                                                               'cart_subtotal': cart_subtotal,
                                                               'tablet': tablet,})

def sale(request):
    context={}
    if request.method == 'POST':
        order_id= request.POST.get('order_id')
        form=SaleForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            o=Sale(
                Serveur=cleaned_data.get('Serveur'),
                Total=cleaned_data.get('Total'),
            )
            o.save()
            context['form']=form
            all_items = LineItem.objects.filter(order_id =order_id)
            for order_item in all_items:
                li = LineItemSale(
                    product_id = order_item.product_id,
                    price = order_item.price,
                    quantity = order_item.quantity,
                    sale_id = o.id
                )
                li.save()
            ci = get_object_or_404(Order, id=order_id)
            ci.delete()          
            return redirect('show_sale')
         
    return render(request, 'ecommerce_app/order.html',context)

def show_sale(request): 
    aujourdhui =datetime.date.today()
    order_items =None
    usernom=User.objects.all() 
    context={}
    context['usernom']=usernom
    if request.method=='POST':
        datet=request.POST.get('datet')
        datet1=request.POST.get('datet1')
        serveur=request.POST.get('serveur')
        if not serveur:
            order_items = Sale.objects.filter(date_addedunique__lte=datet1,date_addedunique__gte=datet)
        else:
            order_items = Sale.objects.filter(date_addedunique__lte=datet1,date_addedunique__gte=datet,Serveur=serveur)
        sub_total = 0
        for item in order_items:
            sub_total += item.Total
        context['sub_total']=sub_total           
    context['order_items']=order_items
    return render(request, 'ecommerce_app/show_sale.html', context)






  
def signin(request):
    if request.user.is_authenticated:
           return redirect('index')
    if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('index')
            elif not(username):
                msg='Username error'
            elif not(password):
                msg='password error'        
            else:
               msg="error de login"
            form=signinForm()
            #AuthenticationForm()
            return render(request,'ecommerce_app/signin.html',{'form':form,'msg':msg})
    else:
        form=signinForm()
        return render(request,'compte/signin.html',{'form':form}) 
      
        
def signout(request):
    logout(request)
    return redirect('index')

def profile(request):
    context={}  
    author_id=request.POST.get('author_id')
    if author_id:
        listeannonce=Announcescar.objects.filter(author_id=author_id)
        context['listeannonce']=listeannonce  
    form = userForm(request.POST,instance=request.user)
    context['form']=form
    return render(request,'compte/profile.html',context)  


"""
if request.method == 'POST':
        postData=request.POST
        Serveur= postData.get('Serveur')
        order_id= postData.get('order_id')
        Total= postData.get('Total')
        form=SaleForm(postData,request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            form.save()
            context['form']=form"""