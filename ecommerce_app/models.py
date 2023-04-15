from django.db import models




class Categories(models.Model):
    categories=models.CharField(max_length=30)
 
    def __str__(self):
        return self.categories

class Numero(models.Model):
    numero=models.CharField(max_length=60)
    def __str__(self):
        return self.numero

class Table(models.Model):
    table=models.CharField(max_length=60)
    numero=models.ForeignKey(Numero,on_delete=models.CASCADE)
 
    def __str__(self):
        return self.table
    


class Product(models.Model):
    name = models.CharField(max_length=191)
    categorie=models.ForeignKey(Categories,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=0)
    slug = models.SlugField()
    quantity = models.IntegerField(blank=True,default=1)
    image = models.ImageField(upload_to='images/', blank=True)
    available= models.BooleanField(default=False,blank=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=0)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def total_cost(self):
        return self.quantity * self.price


class Order(models.Model):
    Table = models.CharField(max_length=191)
    Nom = models.CharField(max_length=191)
    Serveur = models.CharField(max_length=191)
    Tel = models.CharField(max_length=191)
    date_added = models.DateTimeField(auto_now_add=True)
    date_addedunique = models.DateField(auto_now_add=True,blank=True)
    encourspreparation= models.BooleanField(default=False)
    Servir= models.BooleanField(default=False)
    Total= models.IntegerField()

    def __str__(self):
        return "{}:{}".format(self.id, self.Table)

    def total_cost(self):
        return sum([ li.cost() for li in self.lineitem_set.all() ] )


class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=0)
    quantity = models.IntegerField()
    date_addedunique = models.DateField(auto_now_add=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(self.product.order, self.id)

    def cost(self):
        return self.price * self.quantity

class Sale(models.Model):
    Serveur = models.CharField(max_length=191)
    date_added = models.DateTimeField(auto_now_add=True)
    date_addedunique = models.DateField(auto_now_add=True,blank=True)
    Total= models.IntegerField()

  

    def __str__(self):
        return "{}:{}".format(self.id, self.Serveur)

    def total_costsale(self):
        return sum([ li.cost() for li in self.lineItemSale_set.all() ] )

class LineItemSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=0)
    quantity = models.IntegerField()
    date_addedunique = models.DateField(auto_now_add=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}:{}".format(self.product.sale, self.id)

    def cost(self):
        return self.price * self.quantity