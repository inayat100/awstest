from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product,Category,Cart,Address,Order
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from decouple import config


# client = razorpay.Client(auth=('rzp_test_7mPyjnwM8ZduxW','9AsUh5NHIv5NkkuIXZyvudLH'))
client = razorpay.Client(auth=(config('KEY'),config('SECRET')))
# @cache_page(30)
def index(request):
    if request.user.is_authenticated:
        cd = Cart.objects.filter(user_name=request.user).count()
        pdu = Product.objects.all().order_by('?')[:8]
        return render(request, 'index.html',{'products':pdu,'cd':cd})
    pdu = Product.objects.all().order_by('?')[:8]
    return render(request, 'index.html',{'products':pdu,'cd':0})

def sign_up(request):
  if request.method == "POST":
        username = request.POST['username']
        lastname = request.POST['lname']
        firstname = request.POST['fname']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        if password1 != password2:
            messages.error(request, "password must be same both side..")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "This user name alredy taken..")
            return redirect('signup')
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request,"user saveed now.you can login")
        return redirect('signin')
  return render(request,'signup.html',{'cd':0})

def sign_in(request):
 if request.method == "POST":
        user = request.POST['username']
        password = request.POST['pass1']
        user = authenticate(username=user, password=password)
        if user:
            login(request,user)
            messages.success(request,"User successfully Loged in... ")
            return redirect('index')
        else:
            messages.error(request,"user name or password is wrong something....")
            return redirect('singin')
 return render(request,'signin.html',{'cd':0})

def Logout(request):
    logout(request)
    messages.success(request,"User successfully Logout... ")
    return redirect('/')

def full(request):
 sul = request.GET['title']
 pdu = Product.objects.get(ptitle=sul)
 same = Product.objects.filter(cname=pdu.cname).order_by('?')[:8]
 if request.user.is_authenticated:
    if Cart.objects.filter(prd_name = pdu.id).exists() and Cart.objects.filter(prd_name = pdu.id,user_name=request.user).exists():
        obj = Cart.objects.filter(user_name=request.user).count()
        return render(request,'full_page.html',{'product':pdu,'add':True,'same':same,'cd':obj})   
    obj = Cart.objects.filter(user_name=request.user).count()
    return render(request,'full_page.html',{'product':pdu,'same':same,'cd':obj})
 return render(request,'full_page.html',{'product':pdu,'same':same})

def my_address(request):
    if request.user.is_authenticated:
        cd = Cart.objects.filter(user_name=request.user).count()
        al = request.GET.get('all')
        one = request.GET.get('one')
        ad = Address.objects.all()
        if request.method == "POST":
            id = request.POST.get('ads')
            obj = Address.objects.filter(user=request.user)
            for o in obj:
                if o.id == int(id):
                    o.primary = True
                    o.save()
                    continue
                o.primary = False
                o.save()
            if al:    
                return redirect('all_order')
            elif one:
                return redirect(f'/buy/{one}/')
        if al or one:
            return render(request,'address.html',{'add':ad,'dis':True,'cd':cd})
        return render(request,'address.html',{'add':ad,'cd':cd})
    messages.info(request,"you should loging for see your addresss..")
    return redirect('/')

def cat_all(request):
 return render(request,'cat_all.html')

def card(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            a = request.POST.get('card')
            r = request.POST.get('remove')
            if a:
                if Cart.objects.filter(prd_name=a,user_name=request.user):
                    messages.info(request,"item alreday saved in your cart....")
                    return redirect('card')
                uid = User.objects.get(username=request.user)
                pid = Product.objects.get(pk=a)
                cd = Cart(user_name=uid,prd_name=pid)
                cd.save()
                messages.success(request,"item saved into your cart....")
            if r:
                d = Cart.objects.get(pk=r)
                d.delete()
                messages.success(request,"item deleted from your cart....")   
        am = Cart.objects.filter(user_name=request.user).order_by('-id')
        total = 0.0
        for t in am:
            total += (t.prd_name.pprice * t.qty)
        total = round(total,2)
        return render(request,'card.html',{'items':am,'total':total,'cd':am.count()})
    messages.info(request,"you should login to add to cart")
    return redirect('signin')

def add_cart(request):
    if request.user.is_authenticated:
        a = request.GET.get('add')
        obj = Cart.objects.get(pk=a)
        obj.qty += 1
        obj.save()
        upobj = Cart.objects.get(pk=a)
        am = Cart.objects.filter(user_name=request.user)
        total = 0.0
        for t in am:
            total += (t.prd_name.pprice * t.qty)
        total = round(total,2)
        data = {
                "qty":upobj.qty,
                "total":total,
                "cd":am.count(),
        }
        return JsonResponse(data)
    messages.info(request,"sorry you cant hit this url without login")
    return redirect('/')
    
def remove_cart(request):
    if request.user.is_authenticated:
        a = request.GET.get('remove')
        obj = Cart.objects.get(pk=a)
        obj.qty -= 1
        obj.save()
        upobj = Cart.objects.get(pk=a)
        am = Cart.objects.filter(user_name=request.user)
        total = 0.0
        for t in am:
            total -= (t.prd_name.pprice * t.qty)
        total = abs(total)
        total = round(total,2)
        data = {
                "qty":upobj.qty,
                "total":total
        }
        return JsonResponse(data)
    messages.info(request,"sorry you cant hit this url without login")
    return redirect('/')

def buy(request,pk):
    if request.user.is_authenticated:
        cd = Cart.objects.filter(user_name=request.user).count()
        pd = Product.objects.get(pk=pk)
        ad = Address.objects.get(user=request.user,primary=True)
        amount = pd.pprice*100
        payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        return render(request, 'order_sum.html',{'payment':payment,'pk':pd,'ad':ad,'cd':cd})
    messages.info(request,"you should login to buy a product")
    return redirect('signin')

def buy_cart(request):
    if request.user.is_authenticated:
        ad = Address.objects.get(user=request.user,primary=True)
        crd = Cart.objects.filter(user_name=request.user)
        total = 0.0
        for t in crd:
            total += (t.prd_name.pprice * t.qty)
        total = round(total,2)
        amount = round(total,2) * 100
        payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        return render(request, 'cart_buy.html',{'payment':payment,'itm':crd,'ad':ad,'total':total})
    messages.info(request,"you should login to buy a product")
    return redirect('signin')
      
def order_view(request):
    if request.user.is_authenticated:
        cd = Cart.objects.filter(user_name=request.user).count()
        order = Order.objects.filter(user=request.user)
        for o in order:
            print(type(o.order_status))
        return render(request,'order_view.html',{'ord':order,'cd':cd})
    messages.info(request,"you should login to view your orders")
    return redirect('signin')

@csrf_exempt    
def place_order(request):
        if request.method == "POST":
            try:
                print(request.POST)
                pid = request.POST.get('razorpay_payment_id')
                use = request.POST.get('user')
                ad = request.POST.get('add')
                user = User.objects.get(pk=int(use))
                ct = Cart.objects.filter(user_name=user)
                ad = Address.objects.get(pk=int(ad))
                for c in ct:
                    od = Order(user=user,product=c.prd_name,amount=c.prd_name.pprice,payment_id=pid,address=ad,paid=True)
                    od.save()
                    c.delete()
            except  NameError:
                messages.info(request,NameError)
            return HttpResponse("order complated..")
        messages.info(request,"sorry you are using something wrong")
        return redirect('/')
                 
@csrf_exempt
def product_buy(request):
    if request.method == "POST":
        try:
            print(request.POST)
            pid = request.POST.get('razorpay_payment_id')
            pk =  request.POST.get('id')
            us = request.POST.get('user')
            add = request.POST.get('add')
            ad = Address.objects.get(pk=int(add))
            pd = Product.objects.get(pk=int(pk))
            user = User.objects.get(pk=int(us))
            ord = Order(user=user, product=pd,amount=pd.pprice, address=ad,paid=True, payment_id=pid)
            ord.save()
        except NameError:
            messages.info(request,NameError) 
        return HttpResponse("payments done...")
    messages.info(request,"sorry you are using something wrong")
    return redirect('/')

def delet_address(request,pk):
    if request.user.is_authenticated:
        dt = Address.objects.get(pk=pk)
        dt.delete()
        return redirect('my_address')
    messages.error(request,"you cant delet anything without login")
    return redirect('signin')
    
def update_address(request):
    if request.user.is_authenticated:
        cd = Cart.objects.filter(user_name=request.user).count()
        if request.method == "POST":
            name = request.POST.get('name')
            city = request.POST.get('city')
            number = request.POST.get('number')
            pin = request.POST.get('pin')
            home = request.POST.get('home')
            id = request.POST.get('id')
            if id:
                print("update")
                obj = Address.objects.get(pk=id)
                obj.name = name
                obj.phone = number
                obj.city = city
                obj.pin = pin
                obj.house_no = home
                obj.save()
            else:
                print("save")
                ad = Address(user=request.user,name=name,phone=number,city=city,pin=pin,house_no=home)
                ad.save()
            return redirect('my_address')
        id = request.GET.get('update')
        obj = Address.objects.get(pk=id)
        return render(request,'update_address.html',{'a':obj,'cd':cd})
    messages.error(request,"you cant update anything without login")
    return redirect('signin')


def searching(request):
    searching = request.GET['search']
    se1 = Product.objects.filter(scname__icontains=searching)
    se2 = Product.objects.filter(ptitle__icontains=searching)
    se3 = Product.objects.filter(pabout__icontains=searching)
    allproduct = se1.union(se2,se3)
    print(allproduct)
    return render(request,'cat_all.html',{'allp':allproduct})
def test(request):
    pass