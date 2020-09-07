from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template import RequestContext
from .models import Product, ProductImages, Category, Viewer
from .forms import ProductAdd, AddUser, ImageAdd
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.forms import modelformset_factory, formset_factory
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from math import ceil
# Create your views here.


def productlist(request , category_slug = None):
    category = None
    productlist = Product.objects.all()
    categorylist = Category.objects.annotate(total_products=Count('product'))
    
    if category_slug :
        category = get_object_or_404(Category, slug=category_slug)
        productlist = productlist.filter(category=category)


    try:
        search_query = request.GET.get('name')
        search_area = request.GET.get('area')
    except:
        search_query = None
    if search_query:
        productlist = productlist.filter(
            Q(product_name__icontains = search_query) |
            Q(condition__icontains = search_query) |
            Q(brand__icontains = search_query) |
            Q(category__category_name__icontains = search_query)
        )
    
    elif search_area:
        productlist = productlist.filter(
            Q(city__icontains = search_area) |
            Q(country__icontains = search_area)
        )
    

    paginator = Paginator(productlist, 7 ) # Show 15 contacts per page.
    page = request.GET.get('page')
    productlist = paginator.get_page(page)
    template = 'product_list.html'
    context= {'productlist': productlist, 'category_list': categorylist, 'category': category}
    return render(request, template, context)
 






def productdetail(request, product_slug):
    print(product_slug)
    productdetail = Product.objects.get(slug=product_slug)
    productimages = ProductImages.objects.filter(product=productdetail)
    num_visits= request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+ 1
    def get_ip(request):
        adress = request.META.get('HTTP_X_FORWARDED_FOR')
        if adress:
            ip = adress.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_ip(request)
    u = Viewer(product=productdetail ,ip=ip)
    print(ip)
    result = Viewer.objects.filter(
        product=productdetail ,ip=ip
    )
    if len(result)==1:
        print("hello")
    elif len(result)>1:
        print("more")
    else:
        u.save()
        print("work")
    
    count = Viewer.objects.filter(product=productdetail).count
    print("total user: ", count)
    template = 'product_detail.html'
    context = {'product_detail' : productdetail , 'product_images' : productimages, 'num_visits': num_visits, "count": count}
    return render(request , template , context)
@login_required(login_url='/accounts/login')
def contact_view(request):
    return render(request, "contact.html")
@login_required(login_url='/accounts/login')
def contact_views(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        msg = request.POST['msg']
        msgs = ("Thankyou for Contact Us")
        send_mail(
            'HusShu User ' + name + ' Contact Message',
            msg + '\nUser Email-address: ' + email + '\nUser Number: ' + number,
            email,
            ['info.husshu@gmail.com'],
            fail_silently=False
        )
        context = {
            'email': email,
            'name': name,
            'number': number,
            'msg': msg,
            'msgs':msgs
        }
        template = "contact.html"
        return render(request, template, context)
    else:
        return render(request, "contact.html", {})



@login_required(login_url='/accounts/login')
def addproduct(request):
    image_form = ImageAdd(data=request.POST or None, files=request.FILES)
    files = request.FILES.getlist('images')
    product_form = ProductAdd(data=request.POST or None, files=request.FILES)
    if product_form.is_valid() and image_form.is_valid():
        instance = product_form.save(commit=False)
        instance.user = request.user
        instance.save()
        #image.product = instance
        #image.save()
        for f in files:
            img = ProductImages(product = instance, image=f)
            img.save()
        return redirect('/dashboard')
        messages.info(request,'Your Product Added Successfully')
    else:
        product_form = ProductAdd()
        image_form = ImageAdd()
    context = {
        'product_form':product_form,
        'image_form':image_form 
    }
    return render(request, "add_product.html", context)



def howitwork(request):
    return render(request, "how_it_work.html")


def sitemap(request):
    return render(request, "sitemap.html")

def faq(request):
    return render(request, "faq.html")

def terms(request):
    return render(request, "terms.html")

def privacy(request):
    return render(request, "privacy.html")

@login_required(login_url='/accounts/login')
def feedback(request):
    return render(request, "feedback.html")
    
@login_required(login_url='/accounts/login')
def feedbacks(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        number = request.POST['number']
        msg = request.POST['msg']
        msgs = ("Thankyou for your Response")
        context = {
            'email': email,
            'fname': fname,
            'lname': lname,
            'number': number,
            'msg': msg,
            'msgs':msgs
        }
        send_mail(
            'HusShu User ' + fname + lname + ' Feedback',
            msg + '\nUser Email-address: ' + email  + '\nUser Number: ' + number,
            email,
            ['info.husshu@gmail.com'],
            fail_silently=False
        )
        template = "feedback.html"
        return render(request, template, context)
    else:
        return render(request, "feedback.html", {})
def regions(request):
    return render(request, "regions.html")
def popular_search(request):
    return render(request, "popular-search.html")






def index(request , category_slug = None):
    category = None
    categorylist = Category.objects.all()
    productlist = Product.objects.all()
    if category_slug :
        category = get_object_or_404(Category, slug=category_slug)
    else:
        category = Category.objects.all()
    n = len(productlist)
    nslides = n//4 + ceil((n/4)-(n//4))
    context = {'no_of_slides':nslides, 'range': range(1, nslides), 'productlist': productlist, 'categorylist':categorylist,'category': category}
    return render(request, 'index.html', context)



