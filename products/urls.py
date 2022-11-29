from django.contrib import admin
from accounts.views import login_page
from django.urls import path,include
from django.conf.urls.static import static
from products import views
# from django.conf import settings
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #Profile page
    path('view/user/profile/', views.viewuserprofile, name="view_user_profile"),
    path('view/admin/profile/', views.viewadminprofile, name="view_admin_profile"),
    path('edit/profile/', views.editprofile, name="edit_profile"),
    path('edit/profile/admin', views.editprofileadmin, name="edit_profile_admin"),

    #User Site
    path('categoryView/<str:slug>',views.categoryView,name="categoryView"),
    path('search/',views.searchView,name="search"),
    path('view/product/', views.viewproduct, name="view_product"),
    path('view/cart/', views.viewcart, name="view_cart"),
    path('view/order/', views.vieworder, name="view_order"),
    

    # path('add/order/', views.addorder, name="add_order"),
    path('delete/cartitem/<str:uid>', views.deletecart, name="delete_cart_item"),
    path('addto/cart/<str:uid>', views.addtocart, name="addto_cart"),
    path('contact', views.contact, name="contact"),
    path('checkout', views.checkout, name="checkout"),
    path('inc/<str:uid>', views.increase, name="increase"),
    path('dec/<str:uid>', views.decrease, name="decrease"),


    #Admin Site
    path('add/product/', views.addproduct, name="add_product"),
    path('list/product/', views.listproduct, name="list_product"),
    path('update/product/<str:uid>', views.updateproduct, name="update_product"),
    path('delete/product/<str:uid>', views.deleteproduct, name="delete_product"),
    path('list/category/', views.listcategory, name="list_category"),
    path('manage/order/', views.manageorder, name="manage_order"),

    # mail and checkout
    path("mail/",views.mail,name="mail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)