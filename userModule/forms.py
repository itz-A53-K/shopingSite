from django import forms

class signUP_form(forms.Form):
    name= forms.CharField( max_length=100, required=True,label="Your name")

    mobile= forms.CharField( max_length=10, required=True,label="Mobile number")

    email= forms.EmailField( required=True,label="Email" )

    password= forms.CharField( max_length=25,min_length="6", required=True,label="Password",help_text="Password must be at least 6 characters.",widget=forms.PasswordInput(attrs={"placeholder":"Password"}))


class login_form(forms.Form):
    email= forms.EmailField( required=True,label="Email" )

    password= forms.CharField( max_length=25,min_length="6", required=True,label="Password",widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
