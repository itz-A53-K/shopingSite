from django.contrib import admin

from .models import *
# from .models import custom_userModel as User
# Register your models here.


# admin.site.register(userModel)
@admin.register(userModel)# registering custom user model
class userModel(admin.ModelAdmin):
        list_display = ["ph_No",'name','email','is_staff']

@admin.register(subcat_type)
class subcat_type_Model(admin.ModelAdmin):
        list_display = ['type_name','id','FK_product_category']

admin.site.register(product)
admin.site.register(product_category)
admin.site.register(product_subCategory)
admin.site.register(Cart)
admin.site.register(order)
admin.site.register(user_address)
