from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserForm(UserCreationForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    username = forms.CharField(label='User Name')
    email = forms.EmailField(label='Email Address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Your Password...'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Your Password...'}), label='Confirm Password')
    class Meta():
        model = User
        fields = ['first_name' , 'last_name' ,'username' , 'email' , 'password1', 'password2' ]
class Date(forms.ModelForm):
    dob = forms.DateField(widget = forms.DateInput(attrs={'placeholder':'yyyy-mm-dd'}), label='Date of Birth*')
    number = forms.CharField(widget = forms.NumberInput(attrs={'placeholder':'Without hash'}), label='Phone Number*')
    class Meta():
        model = Profile
        exclude = ('user',)
        fields = [
            'dob', 'number'
        ]
class EditUser(forms.ModelForm):
    first_name = forms.CharField(label='First Name*')
    last_name = forms.CharField(label='Last Name*')
    username = forms.CharField(label='Username*')
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label= 'Email*')
    class Meta():
        model = User
        fields = [
            'first_name' , 'last_name' ,'username','email'
        ]

class EditProfile(forms.ModelForm):
    image = forms.ImageField(label="Profile Picture*")
    dob = forms.DateField(label='Date of Birth*')
    number = forms.CharField(widget = forms.NumberInput(attrs={'placeholder':'Without hash'}), label='Phone Number*')
    class Meta():
        model = Profile
        exclude = ('user',)
        fields = [
            'image', 'dob', 'number'
        ]