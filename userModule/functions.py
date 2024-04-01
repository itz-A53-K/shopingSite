from .models import *
import json
from django.db.models import Q

def cartCount(user_id):
    cart = Cart.objects.filter(user_id=user_id)
    cart = cart.count()
    return cart




def subCat_filterList(subCat, allprods):
    
    brands=list()
    for i in allprods:
        brands.append(i.brand_name)
    filterList={"brands":brands}
    return filterList




def getCat(text):
    cat= product_category.objects.get(cat_name__icontains=text)
    return cat

def subCat_list(subCat_type_inp):
    mk= {}
    for sc_type in subCat_type_inp:
        item= product_subCategory.objects.filter(FK_subcat_type= sc_type)

        if  mk.get(sc_type.type_name) == None:
            mk[sc_type.type_name]=list(item)    
    return mk

def nav2_items():
    fashion= subcat_type.objects.filter(Q(FK_product_category=getCat('Clothes')) | Q(FK_product_category=getCat('Footwear')))
    electronic= subcat_type.objects.filter(Q(FK_product_category=getCat('Electronics')) )
    mobile= subcat_type.objects.filter(Q(FK_product_category=getCat('Mobiles')))
    
    params={"Mobile":mobile, "fashion":subCat_list(fashion), "electronic": subCat_list(electronic) }
    return params


