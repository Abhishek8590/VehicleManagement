from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import User

from .models import Vehicle,VehicleImage

class RegisterForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model=User
        fields=["username","email","password1","password2"]

        widgets = {
    'username': forms.TextInput(attrs={'class': 'form-control '}),
    'email': forms.EmailInput(attrs={'class': 'form-control'}),
    
  
    
} 



class LoginForm(forms.Form):
   username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
   password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class PassResetForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password1=forms.CharField(label="new password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label="confirm new password",widget=forms.PasswordInput(attrs={"class":"form-control"}))



class VehicleForm(forms.ModelForm):
    class Meta:
        model=Vehicle
        fields="__all__"
        widgets = {
    'vehicle_number': forms.TextInput(attrs={'class': 'form-control '}),
    'vehicle_type': forms.Select(attrs={'class': 'my-custom-class'}),
    'vehicle_model': forms.TextInput(attrs={'class': 'form-control'}),
    'vehicle_description': forms.Textarea(attrs={'class': 'form-control'}),
    
  
    
} 
  
class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['image']  

