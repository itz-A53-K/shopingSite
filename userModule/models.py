from django.db import models


from django.contrib.auth.models import AbstractUser
from .manager import customUserManager

#admin login admin@ad.ad (1234)
# Create your models here.

class userModel(AbstractUser):
    username= None
    first_name= None
    last_name=None

    email= models.EmailField(unique=True)
    ph_No= models.BigIntegerField(null=True, blank=True,)
    name= models.CharField(null=True, blank=True, max_length=100)
    #delivery_address= models.ForeignKey(user_address, on_delete=models.CASCADE)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS= []

    objects= customUserManager()

    def __str__(self) :
        return self.email

class product_category(models.Model):
    # category=(
    #     ("Electronics" , "Electronics"),
    #     ("Clothes" , "Clothes"),
    #     ("Sports" , "Sports"),
    # )
    id= models.BigAutoField(primary_key=True)
    cat_name= models.CharField(max_length=100)
    # cat_name= models.CharField(max_length=100, choices=category)
    description= models.CharField(max_length=300)

    def __str__(self):
        return self.cat_name
    

class subcat_type(models.Model):
    id=models.BigAutoField(primary_key=True)
    FK_product_category= models.ForeignKey(product_category, on_delete=models.CASCADE)
    type_name= models.CharField(max_length=250)
    # image= models.ImageField(null=True,blank=True, upload_to="Prod_type_Img/")

    def __str__(self) :
        return self.type_name

class product_subCategory(models.Model):
    id=models.BigAutoField(primary_key=True)
    FK_product_category= models.ForeignKey(product_category, on_delete=models.CASCADE, null=True, blank=True)
    FK_subcat_type= models.ForeignKey(subcat_type, on_delete=models.CASCADE, null=True, blank=True)
    subCat_name=models.CharField(max_length=250)
    description= models.CharField(max_length=300)
    
    image= models.ImageField(null=True,blank=True, upload_to="Prod_subCat_Img/")

    def __str__(self):
        return f'{self.subCat_name} (category : {self.FK_product_category} , type "{self.FK_subcat_type})'
    


class product(models.Model):
    
    id= models.BigAutoField(primary_key=True)
    name= models.CharField( max_length=500)
    price= models.FloatField()
    discount_parcent= models.IntegerField(default=0.0, null=True, blank=True)

    FK_product_sub_category= models.ForeignKey(product_subCategory, on_delete=models.CASCADE)
    # FK_seller= models.ForeignKey(seller, on_delete=models.CASCADE)

    quantity_available=models.IntegerField()
    description= models.JSONField(null=True, blank=True)
    description_summary= models.JSONField(null=True, blank=True)

    rating_count= models.IntegerField(default=0,null=True, blank=True)
    review_count= models.IntegerField(default=0,null=True, blank=True)

    seller_name=models.CharField(max_length=200)
    brand_name=models.CharField(max_length=150, null=True, blank=True)

    publish_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    
    image= models.ImageField(null=True,blank=True, upload_to="Prod_Img/")

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    id= models.BigAutoField(primary_key=True)
    FK_product= models.ForeignKey(product, on_delete=models.CASCADE)
    user_id= models.IntegerField()
   


class user_address(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    mobile= models.PositiveIntegerField()
    pincode= models.PositiveSmallIntegerField()
    address= models.CharField( max_length=500)
    city=models.CharField( max_length=50)
    state=models.CharField( max_length=50)
    landmark=models.CharField(null=True, blank=True, max_length=200)

    user= models.ForeignKey(userModel, on_delete=models.CASCADE)


class order(models.Model):
    ORDER_STATUS=(
        ("pending","pending"),
        ("order confirmed","order confirmed"),
        ("shipped","shipped"),
        ("out for delivery","out for delivery"),
        ("delivered","delivered"),
        ("cancellation",(
                ("out for pickup","out for pickup"),
                ("cancelled","cancelled")
            )
         ),
    )
    id=models.BigAutoField(primary_key=True)
    user=models.ForeignKey(userModel, on_delete=models.CASCADE)
    FK_product=models.ForeignKey(product, on_delete=models.CASCADE)
    price=models.FloatField()

    transection_id=models.CharField(max_length=255)
    order_staus=models.CharField(choices=ORDER_STATUS,default='pending' , max_length=50)
    order_time= models.DateTimeField( auto_now_add=True)
    delivery_address= models.ForeignKey(user_address, on_delete=models.CASCADE, null=True, blank=True)
    last_modified_date = models.DateTimeField(auto_now=True)



# class seller(models.Model):
#     # seller_category=(
#     #     ("Electronics" , "Electronics"),
#     #     ("Clothes" , "Clothes"),
#     #     ("Sports" , "Sports"),
#     # )
#     id= models.BigAutoField(primary_key=True)
#     # seller_category= models.CharField(choices=seller_category, max_length=250)
#     seller_name=models.CharField( max_length=500)
#     seller_address= models.TextField()
#     about_seller= models.TextField()
#     def __str__(self):
#         return self.seller_name
    
