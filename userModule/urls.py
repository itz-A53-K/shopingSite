from django.urls import path
from userModule.views import *

urlpatterns = [
    path("", home, name="home" ),

    path("account/", accountView, name="accountView" ),
    path("account/<slug:data>/", accountView, name="accountView" ),
    path("orders/", orderView, name="orderView" ),
    path("order_details/", order_details, name="order_details" ),

    path("view/", viewProd, name="viewProd" ),
    path("view/sub_category/", viewsub_category, name="viewsub_category" ),
    path("view/SC_type/", view_subCat_type, name="view_subCat_type" ),
    path("view/category/", view_category, name="view_category" ),

    path("cart/", cartView, name="cartView" ),

    path("addToCart/", addToCart, name="addToCart" ),
    path("removeFrm_cart/", removeFrm_cart, name="removeFrm_cart" ),

    path("deleteAddress/<int:add_id>", deleteAddress, name="deleteAddress" ),
    path("deleteAddress/", deleteAddress, name="deleteAddress" ),

    path("register/", register, name="register" ),
    path("signIn/", signIn, name="signIn" ),
    path("logout/", logoutHandle, name="logout" ),

    path("sandOTP/", sandOTP, name="sandOTP" ),
    path("verifyOTP/", verifyOTP, name="verifyOTP" ),
]
