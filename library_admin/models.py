from django.db import models

# Create your models here.


class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class Book_Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    image=models.ImageField(upload_to='library/categories/', blank=True)
    No_of_items=models.IntegerField()
    isblocked=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    name=models.CharField(max_length=200,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField()
    category=models.ForeignKey(Book_Category,on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    image1=models.ImageField(upload_to='library/products/', blank=True)
    image2=models.ImageField(upload_to='library/products/', blank=True)
    image3=models.ImageField(upload_to='library/products/', blank=True)
    image4=models.ImageField(upload_to='library/products/', blank=True)

    def __str__(self):
        return self.name
