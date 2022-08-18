from email.mime import image
from django.contrib import admin
from .models import Product,Category,Cart,Address,Order
# Register your models here.
@admin.register(Product)
class products(admin.ModelAdmin):
 list_display = ['id','user','pname','ptitle','pprice']
 
@admin.register(Category)
class products(admin.ModelAdmin):
 list_display = ['id','cname']
 
@admin.register(Cart)
class cart(admin.ModelAdmin):
 list_display = ['id','user_name','prd_name','qty']

@admin.register(Address)
class personal(admin.ModelAdmin):
 list_display = ['id','user','name','phone','city','pin','primary']
 list_editable = ['primary']
 
@admin.register(Order)
class order_list(admin.ModelAdmin):
 list_display = ['id','user','product','order_status','address','amount','paid','datetime']
 list_editable = ['order_status']