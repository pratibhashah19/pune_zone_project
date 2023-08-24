from django import forms
from .models import Customer 
from .models import UploadedFile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.utils.translation import gettext,gettext_lazy as _ 

    
class CustomerRegiForm(UserCreationForm):
    password1=forms.CharField(label="Enter the Password",widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "Enter your password"}))
    
    password2=forms.CharField(label="Enter the Password again",widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "confirm your password"}))
    
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter your Email"}))
    
    class Meta:
        model=User 
        fields=["username","email","password1","password2"]
        label={"email":"Enter the email"}
        widgets={"username":forms.TextInput(attrs={"class":"form-control","placeholder": "Enter Your Username"})}
        
class LoginForm(AuthenticationForm):
        username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,"class":"form-control", "placeholder": "Enter username"}))
        
        password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':True,"class":"form-control", "placeholder": "Enter your password"}))

    
class CustomerProfileForms(forms.ModelForm):
    class Meta:
        model=Customer
        fields=["fullname","mobileno","dob","address","occupation"]
        
        widgets={"fullname":forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter Full Name"}),
                 
        "mobileno":forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter Mobile Number"}),
        
        "dob" :forms.DateInput(attrs={"class":"form-control",'type': 'date'}),

        "address":forms.Textarea(attrs={"class":"form-control","placeholder": "Enter Your address"}),
        
        "occupation":forms.Select(attrs={"class":"form-control","placeholder": "Select Option"}),
        
        # "current_address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter Current Address"}),
        
        "industry": forms.Select(attrs={"class": "form-control"}),
        
        }


