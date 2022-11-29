from unicodedata import category
from webbrowser import get
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# from inventory_management_system import products
from products.models import product
from products.models import category, cart, order
from accounts.models import *
from django.db.models import Q
from accounts.models import User, Profile
import os
from datetime import datetime


from django.core.mail import send_mail

from django.conf import settings

# Create your views here.

# User Site

def searchView(request,user):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(product_name__icontains=query) | Q(product_description__icontains=query)
            results= product.objects.filter(lookups).distinct()
            context={'results': results,
                     'submitbutton': submitbutton}
            return render(request, 'products/search.html', context)
        else:
            return render(request, 'products/search.html')
    else:
        return render(request, 'products/search.html')

def viewproduct(request,user):
    prod= product.objects.all()
    context = {'prod':prod}
    return render(request,'products/viewproduct.html',context)

def categoryView(request,user,slug):
    if(category.objects.filter(slug=slug)):
        category_name = category.objects.filter(slug=slug).first()
        products = product.objects.filter(category__slug=slug)
        context = {'products':products,'category_name':category_name}
        return render(request,"products/category.html",context=context)
    else:
        messages.warning(request,"No such category found")
        return redirect('accounts/userhome.html')

def viewcart(request,user):
    prof=Profile.objects.get(email=user)
    user_id=prof.uid
    
    ct= cart.objects.filter(user_id_c=user_id)
    prod=[]
    quant=[]
    sum=0
    for i in range(len(ct)):
        cart_prod=ct[i].product_id_c
        po=product.objects.get(product_name=cart_prod)
        prod.append(product.objects.get(product_name=cart_prod))
        quant.append(ct[i].quantity)
        p=po.price
        qu=ct[i].quantity
        sum+=float(qu)*p

    mylist=zip(prod,quant)
    context = {'mylist':mylist}  
    co={'mylist':mylist, 'sum':sum}          
    return render(request,'products/cart.html', co)


def deletecart(request,user,uid):
    prod_ob=product.objects.get(uid=uid)
    user_ob=Profile.objects.get(email=user)
    user_cart_items=cart.objects.filter(user_id_c=user_ob)
    for c in user_cart_items:
        if(c.product_id_c==prod_ob):
            c.delete()
            break
        # messages.success(request, 'Product Deleted Successfully')
    return redirect('view_cart', user)

def addtocart(request,user,uid):
    prod_all_ob= product.objects.all()
    context = {'pro':prod_all_ob, 'user':user}

    if request.method=='POST':
        prod_ob=product.objects.get(uid=uid)
        user_ob=Profile.objects.get(email=user)
        user_cart_items=cart.objects.filter(user_id_c=user_ob)
        print("-------------------------------------------")
        print(prod_ob,user_ob,user_cart_items)
        print("-------------------------------------------")

        flag=1
        for item in user_cart_items:
            if (prod_ob==item.product_id_c):
                flag=0
                break
        if(flag==1):
            c=cart()
            c.product_id_c=product.objects.get(uid=uid)
            c.user_id_c=Profile.objects.get(email=user)
            c.save()
            # messages.success(request, 'Product ADDED to Cart')
        else:
            for c in user_cart_items:
                if(c.product_id_c==prod_ob):
                    c.quantity+=1
                    c.save()
                    break
            # messages.success(request, 'Product Already ADDED to Cart')
        return redirect('view_product', user)
    return render(request,'products/viewproduct.html',context)

def increase(request, user, uid):
    prod_ob=product.objects.get(uid=uid)
    user_ob=Profile.objects.get(email=user)
    user_cart_items=cart.objects.filter(user_id_c=user_ob)
    for c in user_cart_items:
        if(c.product_id_c==prod_ob):
            c.quantity+=1
            c.save()
            break
    return redirect('view_cart', user)
    

def decrease(request, user, uid):
    prod_ob=product.objects.get(uid=uid)
    user_ob=Profile.objects.get(email=user)
    user_cart_items=cart.objects.filter(user_id_c=user_ob)
    for c in user_cart_items:
        if(c.product_id_c==prod_ob):
            if (c.quantity>1):
                c.quantity-=1
                c.save()
            else:
                c.delete()
            break

    return redirect('view_cart', user)



def contact(request,user):
    return render(request,'products/contact.html')

def checkout(request,user):
    return render(request,'products/checkout.html')



# Profie Site
def viewuserprofile(request,user):
    prof=Profile.objects.get(email=user)
    context = {'prof':prof}
    return render(request,'products/userprofilepage.html',context)

def viewadminprofile(request,user):
    prof=Profile.objects.get(email=user)
    context = {'prof':prof}
    return render(request,'products/adminprofilepage.html',context)



def editprofile(request,user):
    prof= Profile.objects.get(email=user)
    context = {'prof':prof}
    print(User.username)
    
    if request.method=='POST':
        use=User.objects.get(email=user)
        prof = Profile.objects.get(email=user)
        prof.first_name=request.POST.get('first_name')
        prof.last_name=request.POST.get('last_name')
        prof.email=request.POST.get('email')
        prof.address=request.POST.get('address')
        prof.contact=request.POST.get('contact')
        use.username=request.POST.get('email')
        use.email=request.POST.get('email')
        if len(request.FILES) != 0:
            if prof.profile_image:
                os.remove(prof.profile_image.path)
            prof.profile_image = request.FILES['image']
        prof.save()
        use.save()
        # messages.success(request, "Product Updated Successfully")
        return redirect ('login')
    return render(request,'products/editprofileuser.html',context)



# Admin Site

def editprofileadmin(request,user):
    prof= Profile.objects.get(email=user)
    context = {'prof':prof}
    print(User.username)
    
    if request.method=='POST':
        use=User.objects.get(email=user)
        prof = Profile.objects.get(email=user)
        prof.first_name=request.POST.get('first_name')
        prof.last_name=request.POST.get('last_name')
        prof.email=request.POST.get('email')
        prof.address=request.POST.get('address')
        prof.contact=request.POST.get('contact')
        use.username=request.POST.get('email')
        use.email=request.POST.get('email')
        if len(request.FILES) != 0:
            if prof.profile_image:
                os.remove(prof.profile_image.path)
            prof.profile_image = request.FILES['image']
        prof.save()
        use.save()
        # messages.success(request, "Product Updated Successfully")
        return redirect ('login')
    return render(request,'products/editprofileadmin.html',context)



def listproduct(request,user):
    prod= product.objects.all()
    context = {'prod':prod}    
    return render(request,'products/listproduct.html',context)

def updateproduct(request,user,uid):
    cate= category.objects.all()
    prod=product.objects.get(uid=uid)
    context = {'cate':cate, 'prod':prod}
    
    if request.method=='POST':
        prod = product.objects.get(uid=uid)
        prod.product_name =request.POST.get('product_name')
        prod.category=category.objects.get(uid=request.POST['category'])
        prod.price = request.POST.get('price')
        prod.product_description=request.POST.get('description')
        if len(request.FILES) != 0:
            if len(prod.product_image) > 0:
                os.remove(prod.product_image.path)
            prod.product_image = request.FILES['image']

        prod.save()
        # messages.success(request, "Product Updated Successfully")
        return redirect ('list_product', user)
    return render(request,'products/updateproduct.html',context)

def deleteproduct(request,user,uid):
    prod=product.objects.get(uid=uid)
    context = {'prod':prod}
    prod.delete()
        # messages.success(request, 'Product Deleted Successfully')
    return redirect('list_product', user)


def addproduct(request,user):
    cate= category.objects.all()
    context = {'cate':cate}
    if request.method=='POST':
        prod = product()
        prod.product_name =request.POST.get('product_name')
        prod.category=category.objects.get(uid=request.POST['category'])
        prod.price = request.POST.get('price')
        prod.product_description=request.POST.get('description')
        if len(request.FILES) != 0:
            prod.product_image = request.FILES['image']

        prod.save()
        # messages.success(request, "Product Added Successfully")
        return redirect ('list_product', user)
    return render(request,'products/addproduct.html',context)

def listcategory(request,user):
    return render(request, 'products/listcategory.html')

# Mail

def mail(request,user):
    prof=Profile.objects.get(email=user)
    user_id=prof.uid
    # mail2=user_id_c.email()

    ct= cart.objects.filter(user_id_c=user_id)
    for i in range(len(ct)):
        od=order()
        od.user_id_o=ct[i].user_id_c
        od.product_id_o=ct[i].product_id_c
        od.quantity=ct[i].quantity
        od.orderDate=datetime.now()
        od.save()

    # Mail Sending Using Proton SMTP server

    # subject = 'Order Confirmation'
    # lt= []
    # message="Your order has been confirmed \n Thanks For Using Our Site \n See Order Details Below \n"
    # # lt.append(message)
    # for i in range(len(ct)):
    #     order_prod=ct[i].product_id_c
    #     prod=product.objects.get(product_name=order_prod)
    #     quant=ct[i].quantity
    #     message += str(prod) + "         "+ str(quant)+"\n"
    #     # lt.append(message)


    # message +='''Your order has been confirmed 
    #                 Electo High Store
    # Contact: +91 9041416238, +91 8978216882
    # Email: Saurabh.singh@gmail.com
    # Address: Adesh PG, Near professional courier, Othkalmandapam, Coimbatore '''
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [user]
    # send_mail( subject, message, email_from, recipient_list )

    
    for i in range(len(ct)):
        ct[i].delete()

    # mail mail---------------
        return redirect('checkout', user)



def vieworder(request,user):
    prof=Profile.objects.get(email=user)
    user_id=prof.uid
    od= order.objects.filter(user_id_o=user_id)
    prod=[]
    quant=[]
    date=[]
    for i in range(len(od)):
        order_prod=od[i].product_id_o
        prod.append(product.objects.get(product_name=order_prod))
        quant.append(od[i].quantity)
        date.append(od[i].orderDate)

    mylist=zip(prod,quant,date)
    context = {'mylist':mylist}        
    return render(request,'products/vieworder.html', context)


def manageorder(request,user):
    prof=Profile.objects.get(email=user)
    user_id=prof.uid
    
    od= order.objects.all()
    prod=[]
    quant=[]
    date=[]
    us=[]
    for i in range(len(od)):
        order_prod=od[i].product_id_o
        us.append(od[i].user_id_o)
        
        # us.append(Profile.objects.get(profile_name=user_name))
        prod.append(product.objects.get(product_name=order_prod))
        quant.append(od[i].quantity)
        date.append(od[i].orderDate)

    mylist=zip(prod,quant,date,us)
    context = {'mylist':mylist}        
    return render(request,'products/manageorder.html', context)

