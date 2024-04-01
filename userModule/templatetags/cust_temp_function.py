from django import template
from math import ceil, floor
from ..models import *

import random, string

register = template.Library()

@register.filter
def get_img(value):
    prod_subCat= list(product_subCategory.objects.filter(FK_subcat_type=value))

    if len(prod_subCat) != 0:
        for i in random.sample(prod_subCat, 1):
            return i.image

@register.filter
def get_type(value):
    return type(value).__name__


@register.filter(name= "off_price")
def discount_price(discount_parcent, price):
    
    disc_price= ceil(( (100-discount_parcent) / 100)* price )
    if disc_price%10 == 0 :
        disc_price -=1
    return disc_price



@register.filter(name= "get_rand_item")
def get_rand_item(value, sliceQty ):
    if len(value) <sliceQty:
        sq=len(value)
    else:
        sq= sliceQty
    if type(value) != "list":
        value= list(value)
    return random.sample(value, sq)



@register.filter(name= "order_details_href")
def order_details_href(item_id, ord_id):

    link=f"/order_details/?yt_id={random_string(9)}&item_id={item_id}&o_id=OD{ord_id}&ym_key={random_string(15)}&ref=scl_656430271_5_11"

    link= link.replace(" ","-").replace("'","")
    return link


@register.filter(name= "category_href")
def category_href(cat_id, cat_name):

    link=f"/view/category/?{cat_name}&tns={random_string(15)}&ua_5th={random_string(9)}&cat_id={cat_id}&ywt_key={random_string(15)}&ref=scl_656430271_5_11"

    link= link.replace(" ","-").replace("'","")
    return link

@register.filter(name= "subCat_href")
def subCat_href(subcat_id, subcat_name):

    link=f"/view/sub_category/?{subcat_name}&rdt={random_string(15)}&mh_th={random_string(9)}&subCat_id={subcat_id}&rsl_key={random_string(15)}&ref=scl_656430271_5_11"

    link= link.replace(" ","-").replace("'","")
    return link


@register.filter(name= "subCat_type_href")
def subCat_type_href(type_id, type_name):

    link=f"/view/SC_type/?{type_name}&reoid={random_string(15)}&mit_uye={random_string(9)}&ty_id={type_id}&mst_key={random_string(15)}&ref=scl_656430271_5_11"

    link= link.replace(" ","-").replace("'","")
    return link


@register.filter(name= "prod_href")
def prod_href(id, prodname):

    link=f"/view/?{prodname[:60]}&rdt={random_string(15)}&mh_th={random_string(9)}&p_id={id}&rsl_key={random_string(15)}&ref=pl_656468771_3_77"

    link= link.replace(" ","-").replace("'","")
    return link





@register.filter(name= "get_dict_value")
def get_dict_value(dict, key):
    return dict.get(key)




@register.filter(name= "add_dropLeft_class")
def add_dropLeft_class(value, forloop_counter):
    cls=""
    if forloop_counter > ceil(value / 2):
        cls="dropLeft"
    return cls











def random_string(length):
    str = ''.join(random.choices(string.ascii_letters, k=length))
    return str