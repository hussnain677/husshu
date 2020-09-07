from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.db.models import Count, Q
from .forms import UserForm, EditUser, EditProfile, Date
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.forms import modelformset_factory, formset_factory
from products.models import Product, Viewer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            date_form = Date(data=request.POST)
            if user_form.is_valid() and date_form.is_valid():
                user = user_form.save(commit=False)
                date = date_form.save(commit=False)
                email = user_form.cleaned_data.get('email')
                user.is_active = False
                user.save()
                Profile.objects.create(user = user, dob = date.dob, number = date.number)
                current_site = get_current_site(request)
                email_subject = 'Active your Account'
                message = render_to_string('registration/activate_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': user.id,
                            'token': account_activation_token.make_token(user)
                    })
                email_message = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                email_message.send(fail_silently=False)
                

                #html_content = render_to_string("registration/activate_email.html")
                #text_content = strip_tags(html_content)
                #email = EmailMultiAlternatives(
                    #'Activate Your Account',
                    #text_content,
                    #settings.EMAIL_HOST_USER,
                    #[email],
                    #)
                #email.attach_alternative(html_content,"text/html")
                #email.send(fail_silently=False)
                return render(request, "registration/email_activate.html")
            #else:
              #  messages.info(request, 'Please make sure your onternet connection will be good.')
        else:
            user_form = UserForm()
            date_form = Date()

    context = {'user_form' : user_form, 'date_form':date_form}

    return render(request , 'registration/register.html' , context)


def activate(request, uid, token):
    user = User.objects.get(id=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activate_msg.html', {})
    else:
        return render(request, 'registration/activate_failed.html', {})




def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, ' Your invalid. Please try again.')
            else:
                messages.info(request, ' Your Username/Password is invalid or Your account is not active please check your email')
    context = {}
    return render(request, 'registration/login.html', context)

@login_required(login_url='/accounts/login')
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/accounts/login')
def edit_profiles(request):
    user_form = EditUser(data=request.POST or None, instance=request.user)
    profile_form = EditProfile(data=request.POST or None, instance=request.user.profile, files=request.FILES)
    if user_form.is_valid() or profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('/dashboard')
    else:
        user_form = EditUser(instance=request.user)
        profile_form = EditProfile(instance=request.user.profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request, 'registration/edit.html', context)


@login_required(login_url='/accounts/login')
def dashboard(request):
    if request.user.is_authenticated:
        profile_all = Profile.objects.filter(user__id=request.user.id)
        product_all = Product.objects.filter(user=request.user)
        #views = Viewer.objects.filter(product__in=product_all)
        #views = Viewer.objects.annotate(total_products=Count('product'))
        if len(profile_all)>0:
            data = Profile.objects.get(user__id=request.user.id)
        else:
            data = messages.info(request, ' You have no Product Now add Product.') 
        if len(product_all)>0:
            alls = Product.objects.filter(user=request.user)
        else:
            alls = None
            messages.info(request, ' You have no product add Products and Start Selling.') 
        
    return render(request, 'registration/dashboard.html', {'data':data, 'alls':alls})
    
@login_required(login_url='/accounts/login')
def delete_product(request):
    context = {}
    if "pid" in request.GET:
        pid = request.GET["pid"]
        prd = get_object_or_404(Product, id=pid)
        context["product"] = prd

        if "action" in request.GET:
            prd.delete()
            return redirect('/dashboard')
    return render(request,"registration/deleteproduct.html",context)


def view_404(request, exception):
    return render(request, 'registration/404.html')

