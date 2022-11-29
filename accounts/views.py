from http.client import HTTPResponse
from logging import exception
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from products.models import product
from products.models import category


def login_page(request):
    if request.method == 'POST':     
      
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(request.POST.get('firstname'))

        user_obj = User.objects.filter(username = email)
        print('x'*40)
        print(user_obj)
        print('x'*40)

        if not user_obj.exists():
            messages.warning(request, 'Account Not found. Please Create Account')
            return redirect('/register')
            # return HttpResponseRedirect(request.path_info)
        # if not user_obj[0].profile.is_email_verified:
        #     messages.warning(request, 'Please verify your account')
        #     return HttpResponseRedirect(request.path_info)
     
        user_obj = authenticate(username=email,password=password)        
        if user_obj:
            # username = User.objects.filter(username = email)[0]
            login(request,user_obj)
            if not User.objects.filter(username = email)[0].is_superuser:
                print('- -'*40)
                # username = User.objects.filter(username = email)[0]
                request.session['username'] = email
                # print(product.objects.all()[0].price)
                # request.session['product'] = product.objects.all()[0]
                # print(User.objects.filter(username = email)[0].is_superuser)
                return redirect('/user/'+email)

                # return user_page(request,User.objects.filter(username = email)[0])
                print('- -'*40)
                # print(User.objects.filter(username = email)[0].is_superuser)
            # print('x'*40)
        
            else:
                print('- -'*40)
                print(User.objects.filter(username = email)[0].is_superuser)
                return redirect('/adminpage/'+email)
        # user_obj.save()
        else:
            messages.warning(request, 'Invalid Credential.')
            return HttpResponseRedirect(request.path_info)
    else:
        return render(request,'accounts/login.html')

def user_logout(request):
    
    try:
        
        logout(request)
        messages.success(request, 'Logged out Successfully')
        return HttpResponseRedirect('/login')
    except:
        messages.warning(request, 'some error occured')
        pass
        #message
    
    return redirect('/login')


@login_required
def user_page(request,email):
    print('-+-'*40)
    products = product.objects.all()
    categories = category.objects.all()
    # category = category.objects.all()
    if request.method == 'POST':
        user = User.objects.filter(username = email)[0]
        profile = user.profile

        

    # print(user.contact)
        print(products)
        return render(request,'accounts/userhome.html', {'profile': profile, 'user': user,'products':products,'categories':categories})
    if (request.user.is_authenticated and request.user.profile.email==email):  
        user = User.objects.filter(username = email)[0]
        profile = user.profile

        # print(profile.contact)
        # product=product.objects.all()
        # category = category.objects.all()
        # print(product)
        # return render(request, "accounts/products.html")
        print(products)
        return render(request,'accounts/userhome.html', {'profile': profile, 'user': user,'products':products,'categories':categories})
@login_required
def admin_page(request,email):
    print('-+-'*40)
    products = product.objects.all()
    categories = category.objects.all()
    # category = category.objects.all()
    if request.method == 'POST':
        user = User.objects.filter(username = email)[0]
        profile = user.profile

        print(products)
        return render(request,'accounts/Adminhome.html', {'profile': profile, 'user': user,'products':products,'categories':categories})
    if (request.user.is_authenticated and request.user.profile.email==email):  
        user = User.objects.filter(username = email)[0]
        profile = user.profile

        print(products)
        return render(request,'accounts/Adminhome.html', {'profile': profile, 'user': user,'products':products,'categories':categories})

def register_page(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        print(request.POST.get('firstname'))

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken ')
            return HttpResponseRedirect(request.path_info)
        
        try:
            user_obj = User.objects.create(first_name=firstname,last_name=lastname,email=email,username=email)
            user_obj.profile.email = email
            user_obj.profile.contact = contact
            user_obj.profile.address = address
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request,'Account has been created successfully. You can now Login into Store.')
            return redirect('/login')
            # return HttpResponseRedirect(request.path_info)
        except Exception as e:
            print(e)
            messages.warning(request, 'Phone Number already Exists. Please try with Different Phone Number.')


        # return HttpResponseRedirect(request.path_info)
        # return redirect('/login')
    return render(request,'accounts/register.html')

@login_required
def detailpage(request,email):
    if request.method == 'POST':
        user = User.objects.filter(username = email)[0]
        profile = user.profile
        return render(request,'accounts/profilepage.html', {'profile': profile, 'user': user,})
    if (request.user.is_authenticated and request.user.profile.email==email):  
        user = User.objects.filter(username = email)[0]
        profile = user.profile
        return render(request,'accounts/contact.html', {'profile': profile, 'user': user,})

# def activate_email(request,email):
#     try:
#         user = Profile.objects.get(username=email)
#         user.is_email_verified = True
#         user.save()
#         return redirect('/')
    
#     except Exception as e:
#         return HTTPResponse('Invalid email')