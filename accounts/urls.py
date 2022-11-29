from django.contrib import admin
from accounts.views import login_page,register_page,user_page,user_logout,admin_page
from django.urls import path,include
from django.conf.urls.static import static
from products.urls import *
from accounts import views
# from django.conf import settings
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.login_page, name="login"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('user/<email>/', views.user_page, name="user"),
    path('adminpage/<email>/', views.admin_page, name="admin"),
    path('user/<email>/details/', views.detailpage, name="detailpage"),
    
    
    path('logout/',user_logout,name='logout'),
    # path("user/<email>products/", views.productView, name="ProductView"),
    # path('user/<user>/', user_page, name="user")
    # path('user/<email>', user_page, name="user"),
]
