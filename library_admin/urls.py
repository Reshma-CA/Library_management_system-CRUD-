from django.urls import path
from .import views

urlpatterns = [
    path("",views.admin_signup,name="admin_signup"),
    path("admin_login/",views.admin_login,name = "admin_login"),
    path("admin_home",views.admin_home,name = 'admin_home'),
    # categories pannel

    path("acategories/",views.adminCategory,name='acategories'),
    path("addcategories/",views.addcategories,name='addcategories'),
    path("editcategories/<int:myid>",views.editcategories,name='editcategories'),
    path("deletecategories/<int:myid>",views.deletecategories,name='deletecategories'),
    

    # Product Pannel

    path("aproducts/",views.adminProducts,name='aproducts'),
    path("addproduct/",views.addproducts,name='addproduct'),
    path("editproduct/<int:myid>/",views.editproducts,name='editproduct'),
    path('delete_product/<int:myid>/', views.delete_products, name='delete_product'),

]