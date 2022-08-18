from itertools import product
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

def validate_geeks_mail(value):
    print("what is values here",value)
    if "&" in value or  "#" in value or "+" in value :
        raise ValidationError("This field not accepts spacel charater..#.&.+") 
    else:
        return value
        
def uplo(instance,filename): 
    filename,extension = filename.split('.')
    fname = f"{instance.pname}_{instance.ptitle}"
    fname = fname.replace("/","")
    return 'products/%s.%s' % (fname,extension)    

class Category(models.Model):
    cname = models.CharField(max_length=100)
    def __str__(self):
        return self.cname

class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cname = models.ForeignKey(Category,on_delete=models.CASCADE)
    scname = models.CharField(max_length=60,blank=True,null=True)
    pname = models.CharField(max_length=100)
    ptitle = models.CharField(max_length=200,help_text="plese do not use spacial charater +.#.&",validators=[validate_geeks_mail])
    pimage = models.ImageField(upload_to=uplo)
    pprice = models.FloatField()
    plessprice = models.FloatField(null=True,blank=True)
    pabout = models.TextField(blank=True,null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=70)
    pin = models.CharField(max_length=8)
    house_no = models.CharField(max_length=120)
    primary = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE)
    prd_name = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    @property
    def total(self):
        return self.qty * self.prd_name.pprice

class Order(models.Model):
    CHOICES = (
        ('pending', 'pending'),
        ('confirmed', 'confirmed'),
        ('shipped', 'shipped'),
        ('Delivery', 'Delivery'),
        ('Delivered', 'Delivered'),
    )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    amount = models.CharField(max_length=15)
    paid = models.BooleanField(default=False)
    order_status = models.CharField(max_length=80,choices=CHOICES,default='pending')
    payment_id = models.CharField(max_length=100,blank=True,null=True)
    datetime= models.DateTimeField(auto_now_add=True)
    