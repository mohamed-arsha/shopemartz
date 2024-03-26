from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from app.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import datetime
import sweetify


# Create your views here.
def index(request):
    if 'email' in request.session:
        a = Register.objects.get(email=request.session['email'])
        print(a.id)
        c = Carts.objects.all().filter(user_id=a.id)
        print(c)
        return render(request,'index.html',{'session':request.session['email'],'lencart':len(c)})
    else:
            return render(request,'index.html',{'session':None})
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        passw= request.POST.get('passw')
        b=[]
        a=Register.objects.all()
        for i in a:
            b.append(i.email)
        if email not in b:
            a=Register(uname=uname,email=email,mobno=mobno,passw=passw)
            a.save()
            sweetify.success(request,'Register Successfully')
            return redirect('index')
        else:
            a='Email already registered'
            return render(request, 'register.html',{'error':a})
    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        passw=request.POST.get('passw')
        try:
            a=Register.objects.get(email=email)
            if a.passw == passw:
                request.session['email']=email
                print(request.session['email'])
                sweetify.success(request, 'Login Successfully')
                return redirect('index')
            else:
                a='password incorrect'
                return render(request, 'login.html',{'error':a})
        except:
            a='Email not found'
            return render(request, 'login.html',{'error':a})
    return render(request,'login.html')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        sweetify.success(request, 'Logout Successfully')
        return redirect('index')

def shop(request):
    a=Category.objects.all()
    b=Product.objects.all()
    perimagepage = 6
    pg = request.GET.get('page', 1)
    page=Paginator(b,perimagepage)
    try:
        page_obj=page.page(pg)
        print('h',page_obj)
    except PageNotAnInteger:
        page_obj=page.page(1)
    except EmptyPage:
        page_obj=page.page(page.num_pages)
    if 'email' in request.session:
        r = Register.objects.get(email=request.session['email'])
        print(r.id)
        c = Carts.objects.all().filter(user_id=r.id)
        print(c)
        return render(request,'shop.html',{'session':request.session['email'],'category':a,'page_obj':page_obj,'lencart':len(c)})
    else:
        return render(request,'shop.html',{'session':None,'category':a,'page_obj':page_obj})

def catfilter(request,id):
    a =Category.objects.all()
    b=Product.objects.all().filter(category_id=id)
    perimagepage = 6
    pg = request.GET.get('page', 1)
    page = Paginator(b, perimagepage)
    try:
        page_obj = page.page(pg)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)
    if 'email' in request.session:
        r = Register.objects.get(email=request.session['email'])
        print(r.id)
        c = Carts.objects.all().filter(user_id=r.id)
        print(c)
        return render(request,'shop.html',{'session':request.session['email'],'category':a,'page_obj':page_obj,'lencart':len(c)})
    else:
        return render(request,'shop.html',{'session':None,'category':a,'page_obj':page_obj})

def shop_detail(request,id):

    c=[]
    b=Product.objects.all().filter(category_id=id)
    for i in b:
        c.append(i)
    a=Product.objects.all().filter(id=id)
    print(a)
    for i in a:
        if i in c:
            c.remove(i)
    print(c)
    r=''
    if bool(c) is False:
        r = random.choice(a)
    else:
        r=random.choice(c)
    if 'email' in request.session:
        u = Register.objects.get(email=request.session['email'])
        uid = u.id
        lc = Carts.objects.all().filter(user_id=u.id)
        print(lc)
        quan=None
        try:
            c = Carts.objects.get(user_id=uid, products_id=id)
            quan=c.quantity
        except Carts.DoesNotExist:
            quan=1
        print(quan)
        # q = []
        # c = Carts.objects.all().filter(user_id=uid)
        # for i in c:
        #     q.append(i.quantity)
        # print(q)
        return render(request,'shop_detail.html',{'session':request.session['email'],'product':a,'relprod':r,'quantity':quan,'lencart':len(lc)})
    else:
        return redirect('login')

def cart(request,id):
    if 'email' in request.session:
        print(id)
        r = Register.objects.get(email=request.session['email'])
        print(r.id)
        c = Carts.objects.all().filter(user_id=r.id)
        print(c)
        if request.method == 'POST':
            u=Register.objects.get(email=request.session['email'])
            uid=u.id
            product = Product.objects.get(id=id)
            quantity = request.POST.get('quan')
            print(type(product.price))
            q=int(quantity)
            print(type(q))
            totalprice=product.price*q
            cr=[]
            c=Carts.objects.all().filter(user_id=uid)
            for i in c:
                cr.append(i.products.product_name)
            print(cr)
            if product.product_name in cr:
                Carts.objects.filter(user_id=uid, products_id=id).update(quantity=quantity, total_price=totalprice)
            else:
                a=Carts(user_id=uid,products_id=id,quantity=quantity,total_price=totalprice)
                a.save()
        return redirect('view_cart')
    else:
        return redirect('login')

def view_cart(request):
    if 'email' in request.session:
        a=Register.objects.get(email=request.session['email'])
        c=Carts.objects.all().filter(user_id=a.id)
        b=[]
        for i in c:
            print(i.total_price)
            b.append(i.total_price)
        print(b)
        total_prod_price=sum(b)
        return render(request,'cart.html',{'session':request.session['email'],'carts':c,'lencart':len(c),'total_prod_price':total_prod_price})
    else:
        return render(request,'cart.html',{'session':None})



def decreament(request,id):
    print('id:',id)
    p=Product.objects.get(product_name=id)
    c = Carts.objects.get(products=p.id)
    c.quantity-=1
    tp=c.total_price-c.products.price
    c.total_price=tp
    c.save()
    return redirect('view_cart')

def increment(request,id):
    print('id:',id)
    p=Product.objects.get(product_name=id)
    c = Carts.objects.get(products=p.id)
    c.quantity+=1
    tp=c.total_price+c.products.price
    c.total_price=tp
    c.save()
    return redirect('view_cart')


def deletecartoneitem(request,id):
    print('id:', id)
    p = Product.objects.get(product_name=id)
    c = Carts.objects.get(products=p.id)
    c.delete()
    return redirect('view_cart')


def clearcarts(request):
    a=Register.objects.get(email=request.session['email'])
    c=Carts.objects.all().filter(user_id=a.id)
    c.delete()
    return redirect('view_cart')

def checkout(request):
    if 'email' in request.session:

        a=Register.objects.get(email=request.session['email'])
        c = Carts.objects.all().filter(user_id=a.id)
        b = []
        for i in c:
            print(i.total_price)
            b.append(i.total_price)
        print(b)
        total_prod_price = sum(b)
        return render(request,'checkout.html',{'session':request.session['email'],'carts':c,'total_prod_price':total_prod_price})
    else:
        return redirect('login')

def billing_details(request):
    a=Register.objects.get(email=request.session['email'])
    c=Carts.objects.all().filter(user_id=a.id)
    p=[]
    for i in c:
        p.append(i.orderid)
    if request.method == 'POST':
        country=request.POST.get('country')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zipcode=request.POST.get('postal')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        print(country,fname,lname,address,city)
        card=request.POST.get('card')
        cod=request.POST.get('cod')
        if card is not None and cod is None:
            print('cardpage')
        else:
            c = Carts.objects.all().filter(user_id=a.id)
            for i in c:
                pr = i.products.product_name
                pi=i.products.product_image
                a = Order(user_id=a.id, orderid=i.orderid, prod=pr,product_image=pi ,quantity=i.quantity, country=country,
                          fname=fname, lname=lname, address=address, city=city, state=state, zipcode=zipcode,
                          email=email, phonenumber=phone, total_price=i.total_price,deliverytype='cod')
                a.save()
            return redirect('codordersuccessfully')
        return redirect('checkout')

def codordersuccessfully(request):
    if 'email' in request.session:
        return render(request,'orderplacedsuccess.html',{'session':request.session['email']})
    else:
        return redirect('login')

def myorder(request):
    if 'email' in request.session:
        a = Register.objects.get(email=request.session['email'])
        o = Order.objects.all().filter(user_id=a.id)
        c = Carts.objects.all().filter(user_id=a.id)
        print(o)
        return render(request,'myorder.html',{'session':request.session['email'],'order':o,'lencart':len(c)})
    else:
        return redirect('login')

def category(request):
    a = Category.objects.all()
    if 'email' in request.session:
        r = Register.objects.get(email=request.session['email'])
        c = Carts.objects.all().filter(user_id=r.id)
        return render(request,'category.html',{'session':request.session['email'],'category':a,'lencart':len(c)})
    else:
        return render(request,'category.html',{'session':None,'category':a})


def newarrivals(request):
    p=Product.objects.latest('id')
    if 'email' in request.session:
        r = Register.objects.get(email=request.session['email'])
        c = Carts.objects.all().filter(user_id=r.id)
        return render(request,'newarrivals.html',{'email':request.session['email'],'lencart':len(c),'new':p})
    else:
        return render(request,'newarrivals.html',{'session':None,'new':p})


def contact(request):
    if 'email' in request.session:
        a=Register.objects.get(email=request.session['email'])
        if request.method == 'POST':
            fname=request.POST.get('fname')
            email=request.POST.get('email')
            subject=request.POST.get('subject')
            message=request.POST.get('message')
            c=Contact(fname=fname,email=email,subject=subject,message=message)
            c.save()
            sweetify.success(request,'Contact Successfully')
            return redirect('index')
        return render(request, 'contact.html',{'email':request.session['email'],'profile':a})
    else:
        return redirect('login')


def about(request):
    if 'email' in request.session:
        return render(request,'about.html',{'email':request.session['email']})
    else:
        return render(request,'about.html',{'email':None})
