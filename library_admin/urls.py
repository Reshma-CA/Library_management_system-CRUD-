from django.urls import path
from .import views

urlpatterns = [
    path("",views.admin_signup,name="admin_signup"),
    path("admin_login/",views.admin_login,name = "admin_login"),
    path("admin_home",views.admin_home,name = 'admin_home'),
    path("admin_logout",views.admin_logout,name = 'admin_logout'),
    # categories pannel

    path("acategories/",views.adminCategory,name='acategories'),
    path("addcategories/",views.addcategories,name='addcategories'),
    path("editcategories/<int:myid>",views.editcategories,name='editcategories'),
    path("deletecategories/<int:myid>",views.deletecategories,name='deletecategories'),
     path("blockcategories/<int:myid>",views.blockcategories,name='blockcategories'),
    

    # Product Pannel

    path("aproducts/",views.adminBooks,name='adminbooks'),
    path("addproduct/",views.addBooks,name='addproduct'),
    path("editproduct/<int:myid>/",views.editBooks,name='editproduct'),
    path('delete_product/<int:myid>/', views.delete_Books, name='delete_product'),

]