from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from phone_field import PhoneField

dosage_form = (
    ('Tablet','Tablet'),
    ('Syrup', 'Syrup'),
    ('Suspension', 'Suspension'),
    ('Injection', 'Injection'),
    ('Capsule','Capsule'), 
    )
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True, default='user.png', upload_to='uploads/')
    color = ColorField(default='#FF0000',format="hexa", image_field="image")
    
    
    
    def __str__(self):
        return self.name
        
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url     
        

class Category (models.Model):
    name = models.CharField(max_length=200, null= True)
    indication = models.TextField (max_length=2000,blank=True, null=True,default="ailment")
        
    def __str__(self):
        return str(self.name)
        
class Product(models.Model):
    name = models.CharField(max_length=200, null=True,default="drug")
    drug_class = models.ManyToManyField(Category,default="analgesic")
    price = models.DecimalField(default=1000,max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False,null=True,  blank=False)
    image = models.ImageField(null=True, blank=True, default='sample.png', upload_to='uploads/')
    form = models.CharField (max_length=200,null=True,blank=True,default='Tablet',choices=dosage_form)
    dosage = models.CharField (max_length=200,blank=True,null=True,default="100mg")
    indication = models.TextField (max_length=2000,blank=True, null=True,default="ailment")
    prescription = models.CharField(max_length=1000,blank=True,null=True,default="daily")
    color = ColorField(default='#FF0000',format="hexa", image_field="image")
    views = models.IntegerField(default=0)
    liked = models.ManyToManyField(Customer, default=None, blank= True,  related_name = 'liked')
    
    
    
    def __str__(self):
        return self.name
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url
        
    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE = (
    ('Like','Like'),
    ('Unlike','Unlike'),
    )


class Like (models.Model):
    customer = models.ForeignKey (Customer,on_delete= models.CASCADE)
    product = models.ForeignKey (Product, on_delete = models.CASCADE)
    value = models.CharField (choices = LIKE, default = 'Like', max_length=10)
    
    
    def __str__(self):
        return str(self.product)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,  blank=False)
    transaction_id = models.CharField(max_length=200, null= True)
        
    def __str__(self):
        return str(self.id)
        
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
             
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
       
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total     
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True,  blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField (max_length=200, null=False,default="nigeria")
    city = models.CharField (max_length=200, null=False)
    state = models.CharField (max_length=200, null=False)
    zipcode = models.CharField (max_length=200, null=False)  
    date_added = models.DateTimeField(auto_now_add=True)
    
                   
    def __str__(self):
        return self.address      
        
        
        
class ThemeSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField (max_length=200)
    value = models.CharField (max_length =200)
    
    def __str__(self):
        return self.name
