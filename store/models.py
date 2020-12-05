from django.db import models
import datetime


# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    
    def isExists(self):
      if Customer.objects.filter(email=self.email):
        return True
      else:
        return False


    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False



class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=200,default='')
    image = models.ImageField(upload_to = 'upload_to/products/')

    @staticmethod
    def get_all_products():
    	return Product.objects.all()

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)


    @staticmethod
    def get_all_products_by_categoryid(category_id):
    	if category_id:
    		return Product.objects.filter(category=category_id)
    	else:
    		return Product.get_all_products()


class Orders(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cutomer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=100,default='',blank=True)
    phone = models.CharField(max_length=50,default='',blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default = False)

    


    @staticmethod
    def get_orders_by_customer(cutomer_id):
        return Orders.objects.filter(cutomer = cutomer_id).order_by('-date')

   

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)



        
        




   
