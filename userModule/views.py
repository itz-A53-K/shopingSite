from django.shortcuts import render, redirect
from django.http import JsonResponse,Http404,HttpResponse
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
from django.db.models import Q
from django.core import serializers

from .models import *
from .functions import *
from .forms import *
from math import ceil

import random, requests


siteName="siteName"
usr= "userModule"
# Create your views here.
def home(request):
    
    manJeans= product.objects.filter(FK_product_sub_category= 9)[:20]
    msk= product.objects.filter()
    topDealProd=[ msk]

    bestElectronics= product_subCategory.objects.filter(Q(FK_product_category=3) | Q(FK_product_category=1) )[0:10]
    
    params={"topDealProd": list(topDealProd), "manJeans":list(manJeans), "cartCount":cartCount(request.user.id), "bestElectronics":list(bestElectronics), "nav2_items":nav2_items()}
    return render(request,usr+'/index.html', params)


def viewProd(request):      
    if request.method == 'GET':
        p_id= request.GET.get("p_id")
        prod= product.objects.get(id= p_id)

        if prod.discount_parcent == 0 or prod.discount_parcent is None:
            discount_price=0
        else:
            discount_price= ceil(( (100-prod.discount_parcent) / 100)* prod.price )
            if discount_price%10 == 0:
                discount_price -=1
        

        prod_cat=product_category.objects.get(id=(prod.FK_product_sub_category.FK_product_category.id))

        prod_subCat=product_subCategory.objects.get(id=(prod.FK_product_sub_category.id))

        reco_category=""
        if (prod.FK_product_sub_category.FK_product_category.cat_name) == "Clothes":
            if "Women" in (prod.FK_product_sub_category.subCat_name):
                reco_category=product_subCategory.objects.filter(Q(FK_product_category=prod_cat) & ~Q(subCat_name__icontains="Men"))[0:10]
            else:
                reco_category=product_subCategory.objects.filter(Q(FK_product_category=prod_cat) & ~Q(subCat_name__icontains="Women"))[0:10]
        else:
            reco_category=product_subCategory.objects.filter(Q(FK_product_category=prod_cat) & ~Q(id=prod.FK_product_sub_category.id))[0:10]


        similar_prod=product.objects.filter(Q(FK_product_sub_category =prod_subCat) & ~Q(id= p_id))[0:20]

        prodInCart=Cart.objects.filter(FK_product= prod, user_id=request.user.id).exists()
       

        params={"p_id":p_id,"prod":prod,"discount_price":discount_price, "inr":[1,2,2,2,2,2,2,2],"prodInCart":prodInCart, "cartCount":cartCount(request.user.id), "reco_category":reco_category, "similar_prod":similar_prod, "nav2_items":nav2_items()}

        return render(request,usr+'/productView.html',params)
    else:
        return redirect("/")
    

def viewsub_category(request):      
    if request.method == 'GET':
        subCat_id= request.GET.get("subCat_id")

        sub_cat= product_subCategory.objects.get(id=subCat_id)
        allprod_under_cat= product.objects.filter(FK_product_sub_category= sub_cat)
        
        params={"p_id":subCat_id,"allprod_under_cat":allprod_under_cat, "cartCount":cartCount(request.user.id),"sub_category":sub_cat, "filters":subCat_filterList(sub_cat,allprod_under_cat), "nav2_items":nav2_items()}

        return render(request,usr+'/subCat_prod_View.html',params)
    else:
        return redirect("/")
    

def view_subCat_type(request):      
    if request.method == 'GET':
        subCat_type_id= request.GET.get("ty_id")

        subCat_type= subcat_type.objects.get(id=subCat_type_id)
        all_subCat_under_type= product_subCategory.objects.filter(FK_subcat_type=subCat_type_id)

        allprod_under_type={}
        for subcat in all_subCat_under_type:

            allprod= list(product.objects.filter(FK_product_sub_category=subcat))
            
            if  allprod_under_type.get(subcat.subCat_name) == None:
                allprod_under_type[subcat.subCat_name]=allprod  

        params={"all_subCat_under_type":all_subCat_under_type,"subCat_type":subCat_type,"allprod_under_type":allprod_under_type, "cartCount":cartCount(request.user.id), "nav2_items":nav2_items()}

        return render(request,usr+'/subcat&prod_under_type_view.html',params)
    else:
        return redirect("/")


def view_category(request):
    if request.method == 'GET':
        cat_id= request.GET.get("cat_id")

        category= product_category.objects.get(id=cat_id)
        all_subCat_type_under_cat= subcat_type.objects.filter(FK_product_category=category)

        all_subCategory={}
        for SC_type in all_subCat_type_under_cat[:3]:
            sub_category= product_subCategory.objects.filter(FK_subcat_type= SC_type)
            if len(sub_category) > 1:
                if  all_subCategory.get(SC_type.type_name) == None:
                    all_subCategory[SC_type.type_name]=list(sub_category)  
    

        params={"category": category, "all_subCat_type_under_cat": all_subCat_type_under_cat,"all_subCategory": all_subCategory, "cartCount":cartCount(request.user.id), "nav2_items":nav2_items()}

        return render(request,usr+'/category_view.html', params)
    else:
        return redirect("/")
    



def cartView(request):
    
    cartObj= Cart.objects.filter(Q(user_id= request.user.id)).order_by('-id')
    totalAmt=0
    amt_aft_disc=0
    total_disc_amt=0
    for i in cartObj:
        if i.FK_product.quantity_available != 0:
            if i.FK_product.discount_parcent == 0 or i.FK_product.discount_parcent is None:
                discount_price=0
                item_dis_amt=0
            else:
                discount_price= ceil(( (100-i.FK_product.discount_parcent) / 100)* i.FK_product.price )
                if discount_price%10 == 0:
                    discount_price -=1
                item_dis_amt= i.FK_product.price - discount_price

            total_disc_amt += item_dis_amt
            totalAmt += i.FK_product.price

    amt_aft_disc += totalAmt- total_disc_amt

    params={"cartObj":cartObj,"cartCount":cartCount(request.user.id), "nav2_items":nav2_items(),"total_disc":total_disc_amt, "amt_aft_disc": amt_aft_disc, "total_Amt": totalAmt}

    return render(request,usr+'/cartView.html', params)




def orderView(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first !!")
        return redirect('/signIn')
    # orderView_items=list(order.objects.filter(Q(user=request.user)))
    

    if request.method == 'GET':
        order_status= request.GET.get("order_status")
        query=Q()
        if order_status =="On the way":
            query= Q(order_staus='order confirmed') | Q(order_staus='shipped') | Q(order_staus='out for delivery') 
        
        elif order_status =="Delivered":
            query= Q(order_staus='delivered')

        elif order_status =="Cancelled":
            query= Q(order_staus='out for pickup') | Q(order_staus='cancelled')

        orderView_items= order.objects.filter(Q(user= request.user) & query).order_by("-id")
    
        filters={"ORDER STATUS": ["All","On the way","Delivered","Cancelled"],"ORDER TIME":[]}

        params={"orderView_items":orderView_items,"order_status":order_status, "cartCount":cartCount(request.user.id), "nav2_items":nav2_items(),"filters":filters}
        return render(request,usr+'/orderView.html', params)


def order_details(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first !!")
        return redirect('/signIn')
    
    return render(request,usr+'/order_details.html')


def accountView(request, data=None):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first !!")
        return redirect('/signIn')
    
    active="profile"
    dataFor_temp = ""
    # if request.method == 'GET':
    if data == None:
        user= userModel.objects.get(id= request.user.id)
        dataFor_temp= user

        if request.method == 'POST':
            if request.POST.get("frm") == "info_frm":
                try:
                    user.name= request.POST.get("name")
                    user.ph_no= request.POST.get("ph_no")                
                    user.save()
                    messages.success(request, "Profile updated successfully.")
                except:
                    messages.error(request, "Some error occurred! Please try again.")
                    
        
            if request.POST.get("frm") == "ac_frm":

                authUser= authenticate(request, email=request.user.email, password=request.POST.get('cur_pass'))

                if authUser is not None:
                    user.set_password(request.POST.get('new_pass'))
                    user.save()
                    logout(request)
                    messages.success(request, "Password changed. Please login with the new password.")
                    return redirect("/signIn")
                else:
                   messages.error(request,"You have entered wrong password!!")

            return redirect("/account")
    
    elif data == "addressBook":
        active= "addressBook"

        if request.method == 'POST':
            name=request.POST.get("name_add")
            phone=request.POST.get("ph_add")
            pincode=request.POST.get("pincode_add")
            city=request.POST.get("city_add")
            addr_inp=request.POST.get("address")
            state=request.POST.get("state_add")
            landmark=request.POST.get("landmark_add")
            addr_id= request.POST.get("addr_id")

            
            if request.POST.get("addr_frm_use") == "add_n_addr":
                addrExist= user_address.objects.filter(mobile= phone, user= request.user).exists()

                if not addrExist:

                    newAddr= user_address.objects.create(name=name, mobile= phone, pincode= pincode, address= addr_inp, city= city, state= state, landmark= landmark, user= userModel.objects.get(id= request.user.id))
                    newAddr.save()
                    messages.success(request, "New address added successfully.")
                    return redirect("/account/addressBook/")
                else:
                    messages.error(request, "Address already exists with this mobile number !")


            elif request.POST.get("addr_frm_use") == "edit_addr":
                
                addrExist= user_address.objects.filter(id=addr_id, user= request.user).exists()
                if  addrExist:

                    editAddr= user_address.objects.filter(id=addr_id).update(name=name, pincode= pincode, address= addr_inp, city= city, state= state, landmark= landmark)
                    # editAddr.save()

                    messages.success(request, "Address edited successfully.")
                    return redirect("/account/addressBook/")
                else:
                    messages.error(request, "Address do not exists !")
            

            elif request.POST.get("addr_frm_use") == "get_edit_addr_edit":

                addrExist= user_address.objects.filter(id= addr_id, user= request.user).exists()
                addrList=list()
                success= False
                if addrExist:
                    addrObj= user_address.objects.get(user= request.user, id=addr_id)

                    addrList={"addr_id":addrObj.id, "name_add":addrObj.name,"ph_add":addrObj.mobile,"pincode_add":addrObj.pincode,"city_add":addrObj.city,"address":addrObj.address,"state_add":addrObj.state,"landmark_add":addrObj.landmark}

                    success=True
                    
                return JsonResponse({"success":success,"addr":addrList})
                
           

        all_Address= user_address.objects.filter(user= request.user).order_by("-id")
        dataFor_temp= all_Address

    
    params={"active":active,"dataFor_temp":dataFor_temp,  "cartCount":cartCount(request.user.id), "nav2_items":nav2_items()}

    return render(request,usr+'/accountView.html', params)
    # else:
    #     return Http404





def addToCart(request):
    if request.method == 'POST':
        suc= False
        msg= "unauth"
        if request.user.is_authenticated:
            
            product_Inst= product.objects.get(id=request.POST.get("p_Id"))
            user_id=request.user.id

            checkProdExists= Cart.objects.filter(FK_product= product_Inst, user_id=user_id).exists()

            if not checkProdExists:
                cart = Cart.objects.create(FK_product= product_Inst, user_id=user_id)
                cart.save()
                suc= True
                msg="Product added to cart"
                messages.success(request, "1 Item added to cart")
            else:
                msg="Product already in cart !!"
        else:
            messages.error(request, "Please Login First !!")  
                 
        return JsonResponse({"success":suc,"msg":msg, "cartCount":cartCount(request.user.id)})
    else:
        return Http404

def removeFrm_cart(request):
    msg="Bad request 😡!!"
    success= False
    if not request.user.is_authenticated:
        messages.error(request,"Please Login first !!")
        msg="unauth"
    else:
        if request.method == 'POST':
            c_id= request.POST.get("c_id")

            itemExist = Cart.objects.filter(id= c_id, user_id= request.user.id).exists()
            if itemExist:
                item= Cart.objects.get(id=c_id,user_id= request.user.id)
                item.delete()
                msg="successfully removed"
                messages.success(request, "Item removed from cart successfully")
                success= True
            else:
                msg="No item found !"
        else:
            pass
        
    return JsonResponse({"success":success, "msg": msg, "cartCount":cartCount(request.user.id)})


def deleteAddress(request, add_id = None):
    if not request.user.is_authenticated:
        
        return redirect('/')
    
    if add_id == None:
        messages.error(request, "Bad request 😡!!") 
    else:
        addressExist= user_address.objects.filter(user= request.user, id= add_id).exists()
        if addressExist:
            address= user_address.objects.get(user= request.user, id= add_id)
            address.delete()

            messages.success(request, "Address deleted successfully.") 
        else:
            messages.error(request, "Some error occurred ! Please try again.") 
    
    return redirect("/account/addressBook")











def register(request):
    if request.method == "POST":
        name= request.POST.get("name")
        phone= request.POST.get("phone")
        email= request.POST.get("email")
        password= request.POST.get("password")

        accountExists= userModel.objects.filter(email=email).exists()
        
        if not accountExists:
            account=userModel.objects.create_user(email=email, ph_No=phone,name=name, password=password)
            account.save()

            messages.success(request,"Account created successfully. Login now")
            return redirect("/signIn/")
        messages.error(request, "Account already exists. Please login")
    
    return render(request,usr+'/register.html',{"cartCount":cartCount(request.user.id)})


def signIn(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':

        form = login_form(request.POST)
        if form.is_valid():
            email= form.cleaned_data["email"]
            password= form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None :
                login(request, user)
                messages.success(request, "You have loggedin successfully")
                return redirect('/')

            else:
                messages.error(request, "Invalid credentials.")
                return redirect("/signIn")
    
    return render(request, usr+'/login.html',{"login_form":login_form,"cartCount":cartCount(request.user.id)})

def logoutHandle(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have logged out successfully.")
        return redirect('/')
    

def verifyOTP(request):
    if request.method=="POST":
        if not request.user.is_authenticated:

            inputOTP= request.POST.get('inputOTP')
            resetpass_generated_OTP = request.session['regi_generated_OTP']

            inputEmail = request.POST.get('inputEmail')
            resetpass_email = request.session['regi_email']
            if int(inputOTP) == resetpass_generated_OTP and inputEmail== resetpass_email:
                try:
                    #deleting sessions
                    del request.session['regi_generated_OTP']
                    del request.session['regi_email']
                    print("session dlt")
                except:
                    print("session can't be deleted")

                
                return JsonResponse({'success': True, 'msg': 'OTP verify success.'})
            else:
                return JsonResponse({'success': False, 'msg': 'OTP do not match! Please enter valid OTP.'})
    else:
        return redirect('/')

def sandOTP(request):
    msg= 'Bad request'
    success= False
    if request.method=="POST" :
        msg= 'user already logged in !'
        if not request.user.is_authenticated:
            inp_email= request.POST.get('inputEmail')
            
            otp= random.randint(100000 ,999999)
            msg= f'''Hello Dear,

    Thank you for signing in with {siteName}. We want to make sure it's really you. Your One-Time Password (OTP) to complete the registration process is {otp} (Valid only for 5 minutes). Please do not share the OTP with anyone.
    If you don't want to create an account, you can ignore this message. 

    Thank you,
    Team {siteName}                       
   '''                         
            resp= send_mail(
                f'{siteName} authentication',
                msg,
                'test.mailotp96@gmail.com',
                [inp_email],
                fail_silently=False,
            )
            if resp== 1:
                request.session['regi_generated_OTP']= otp
                request.session['regi_email']=inp_email
                
                msg= f'An Email with a verification code sent to your email address "{inp_email}"'
                success=True
            else:
                msg= "Email could't be sant! Please try again. "
        
    return JsonResponse({'msg': msg, 'success': success})
    

