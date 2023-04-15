from django.contrib import admin
from .models import Product, Order, CartItem, LineItem,Categories,Sale,LineItemSale,Table,Numero

# Register your models here.
class CategoriesAdmin(admin.ModelAdmin):
    list_display =['id', 'categories']


#class ProductAdmin(admin.ModelAdmin):
#    list_display =['id', 'name', 'price','available','quantity']

class TableAdmin(admin.ModelAdmin):
    list_display =['id', 'table','numero']

class NumeroAdmin(admin.ModelAdmin):
    list_display =['id', 'numero']




class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'Table', 'Nom', 'date_added', 'encourspreparation', 'Servir','Total']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'product']

class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'Serveur', 'date_added','Total']


class LineItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'date_added', 'order']

class LineItemSaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'date_added', 'sale']



admin.site.register(Table,TableAdmin)
admin.site.register(Numero,NumeroAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem, OrderItemAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(LineItemSale, LineItemSaleAdmin)


@admin.register(Product)
class produits(admin.ModelAdmin):
    list_display=('name','slug','categorie', 'price','available','quantity','image')
    list_filter=('categorie','available')
    orderimg=('-name')
    fieldsets=( 
               ("liste des produits",{
                  "fields":('name','slug','categorie','price','available','quantity','image')
                   
               }),
        
   )











