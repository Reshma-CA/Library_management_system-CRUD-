from django.shortcuts import render

# Create your views here.

# def adminlogin(request):
#     return render(request,'signin.html')

from django.shortcuts import render, redirect
from .forms import AdminSignupForm
from .models import Admin
from .models import Book_Category
from .models import Book
from .forms import AdminLoginForm
from django.views.decorators.cache import never_cache
from django.db import IntegrityError  # Import IntegrityError
import os
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            # Check if email already exists
            email = form.cleaned_data['email']
            if Admin.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'form': form, 'error': 'Email already exists.'})
            
            # Save admin details if email doesn't exist
            form.save()
            return redirect('admin_login')
    else:
        form = AdminSignupForm()
    
    return render(request, 'signup.html', {'form': form})




# def admin_login(request):
#     if request.method == 'POST':
#         form = AdminLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
            
#             # Check if admin with provided credentials exists
#             if Admin.objects.filter(email=email, password=password).exists():
#                 # Perform login action (you might want to use Django's authentication framework)
#                  # session creation
#                 return redirect('admin_home')  # Replace 'dashboard' with your actual admin dashboard URL
#             else:
#                 return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password.'})
#     else:
#         form = AdminLoginForm()
    
#     return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import AdminLoginForm
from .models import Admin

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if admin with provided credentials exists
            try:
                admin = Admin.objects.get(email=email, password=password)
            except Admin.DoesNotExist:
                admin = None

            if admin is not None:
                # Perform login action (you might want to use Django's authentication framework)
                
                # Create a session for the admin
                request.session['admin_id'] = admin.id
                request.session['admin_email'] = admin.email

                return redirect('admin_home')  # Replace 'admin_home' with your actual admin dashboard URL
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password.'})
    else:
        form = AdminLoginForm()
    
    return render(request, 'login.html', {'form': form})


def admin_home(request):
    return render(request,'adminhome.html')

@never_cache  
def adminCategory(request):
    # Retrieve all categories from the database
    categories = Book_Category.objects.all()

    if request.method == "POST":
        # Handle the search functionality
        search_item = request.POST.get("searchitem")
        categories = Book_Category.objects.filter(name__istartswith=search_item)

        context = {
        'datas': categories,
    }


    return render(request, "categories/categories.html",{'datas':categories})

def addcategories(request):
    categoryobjs = Book_Category.objects.all()
   
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get("name",None)
        No_of_items = request.POST.get("No_of_items",None)  # Make sure the 'name' attribute matches your HTML form
        image = request.FILES.get("image",None)
        error = {}
        if name == None or No_of_items == None or image == None:
            error['empty']="Can't submit empty form"
            return render(request, "categories/addcategories.html", {"error": error})
        

        if Book_Category.objects.filter(name=name).exists():
            
            error["name"] = "Same Category name is not allowed"
        elif len(name) > 20:
            error["name"] = "Category name can at most have 20 letters"
        else:
            try:
                added = Book_Category(name=name, No_of_items=No_of_items , image=image)
                added.save()
                return redirect('acategories')
            except IntegrityError:
                error["name"] = "Category with this name already exists"

        return render(request, "categories/addcategories.html", {"error": error})

    return render(request, "categories/addcategories.html", {"categoryobjs": categoryobjs})



def editcategories(request, myid):
    obj = Book_Category.objects.get(id=myid)
    categoryobjs = Book_Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        No_of_items = request.POST.get("No_of_items")  # Use "No_of_items" consistently with your form
        error = {}

        if Book_Category.objects.filter(name=name).exclude(id=myid).exists():
            error["name"] = "Same Category name is not allowed"
        elif len(name) > 20:
            error["name"] = "Category name can have at most 20 letters"
        else:
            obj.name = name
            obj.No_of_items = No_of_items
            if 'image' in request.FILES:
                # Delete the existing image file
                if obj.image:
                    os.remove(obj.image.path)
                obj.image = request.FILES.get('image')
            obj.save()
            return redirect('acategories')
        if error:
            return render(request, "categories/editcategories.html", {"obj": obj, "error": error, "categoryobjs": categoryobjs})

    return render(request, "categories/editcategories.html", {"obj": obj, "categoryobjs": categoryobjs})

def deletecategories(request, myid):
    category = get_object_or_404(Book_Category,id=myid)
    if request.method == "POST":
        # Delete the product if the request method is POST
        category.delete()
        return redirect('acategories')
    context = {
        'content': category,

    }

    return render(request, "tadmin/categories/deletecategories.html",{'content':category})


def addproducts(request):
    categoryobjs = Book_Category.objects.all()
    error = {}

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        category_name = request.POST.get("category")
        description = request.POST.get("description")
        image1 = request.FILES.get("image1")
        image2 = request.FILES.get("image2")
        image3 = request.FILES.get("image3")
        image4 = request.FILES.get("image4")

        try:
            # Check for minimum length requirements
            if len(name) < 4:
                raise ValidationError("Product name should contain a minimum of four characters")

            # Ensure price and quantity are numeric
            if not price.isdigit():
                raise ValidationError("Price must be a numeric value")
            if not quantity.isdigit():
                raise ValidationError("Quantity must be a numeric value")

            # Check if category exists
            categoryobject = Book_Category.objects.get(name=category_name)
        except (ValidationError, Book_Category.DoesNotExist) as e:
            error["general"] = str(e)
        else:
            # Create the product
            product = Book.objects.create(
                name=name,
                category=categoryobject,
                description=description,
                quantity=quantity,
                price=price,
                image1=image1,
                image2=image2,
                image3=image3,
                image4=image4
            )
            return redirect('aproducts')

    return render(request, "tadmin/products/addproducts.html", {"error": error, "categoryobjs": categoryobjs})

def editproducts(request,myid):
    content = Book.objects.get(id=myid)
    categoryobjs = Book_Category.objects.all()
    error = {}

    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        category_name = request.POST.get("category")
        description = request.POST.get("description")

        if len(name) < 4:
            error["name"] = "Product name should contain a minimum of four characters"
    
        else:
            content.name = name
            content.description = description
            content.price = price
            content.quantity = quantity

            # Check if new images are provided
            if 'image1' in request.FILES:
                # Delete the existing image1 file
                if content.image1:
                    os.remove(content.image1.path)
                content.image1 = request.FILES.get('image1')

            if 'image2' in request.FILES:
                # Delete the existing image2 file
                if content.image2:
                    os.remove(content.image2.path)
                content.image2 = request.FILES.get('image2')

            if 'image3' in request.FILES:
                # Delete the existing image3 file
                if content.image3:
                    os.remove(content.image3.path)
                content.image3 = request.FILES.get('image3')

            if 'image4' in request.FILES:
                # Delete the existing image4 file
                if content.image4:
                    os.remove(content.image4.path)
                content.image4 = request.FILES.get('image4')

            # Retrieve the category if it exists, otherwise assign a default category
            try:
                categoryobject = Book_Category.objects.get(name=category_name)
            except Book_Category.DoesNotExist:
                error["category"] = "Invalid category"
            else:
                content.category = categoryobject
                content.save()
                return redirect('aproducts')

        if error:
            return render(request, "books/editproducts.html", {"content": content, "error": error, "categoryobjs": categoryobjs})

    return render(request, "books/editproducts.html", {"content": content, "categoryobjs": categoryobjs})
    

@never_cache
def adminProducts(request):
    if "ausername" in request.session:
        datas = Book.objects.all()
        page = request.GET.get('page')  # Get the current page number from the request's GET parameters
        per_page = 10  # You can change this to your desired number of items per page

        if request.method == "POST":
            enteredproduct = request.POST.get("searchitem")
            datas = Book.objects.filter(name__istartswith=enteredproduct)

        paginator = Paginator(datas, per_page)
        try:
            datas = paginator.page(page)
        except PageNotAnInteger:
            datas = paginator.page(1)
        except EmptyPage:
            datas = paginator.page(paginator.num_pages)

        return render(request, "books/products.html", {"datas": datas})
    else:
        return redirect('admin_login')
    




def delete_products(request,myid):
    product = get_object_or_404(Book, id=myid)
    if request.method == 'POST':
        # Delete the product if the request method is POST
        product.delete()
        return redirect('aproducts')  # Redirect to the product list page after deletion
    context = {
        'content': product,
    }

    return render(request, 'books/deleteproducts.html', {'content': product})
   

    