"""olx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls import url, handler404
from accounts import views
from products.views import index, contact_view, addproduct, contact_views, sitemap, faq, howitwork, terms, privacy, regions, feedback, popular_search, feedbacks
from django.views.static import serve
admin.site.site_header = 'HusShu'
admin.site.site_title = 'HusShu'
admin.site.index_header = 'HusShu'
admin.site.index_title = 'HusShu database'

handler404 = 'accounts.views.view_404'


urlpatterns = [
    path('accounts/login/' , views.loginView , name='login'),
    path('activate/<uid>/<token>',views.activate, name='activate'),
    path('dashboard/delete' , views.delete_product , name='delete_product'),
    path('accounts/register/' , views.register , name='register'),
    path('accounts/logout/' , views.logout , name='logout'),
    path('dashboard/' , views.dashboard , name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls'), name='account'),
    path('dbhusshu/', admin.site.urls),
    path('accounts/', include('accounts.urls' , namespace='accounts')),
    path('accounts/edit/' , views.edit_profiles , name='edit_profiles'),
    path('products/', include('products.urls', namespace='products')),
    path('add_product/', addproduct, name='addproduct'),
    #path('add_product/success/', addimage, name='addimage'),
    path('', index , name='index'),
    path('contact/', contact_view, name='contact'),
    path('howitwork', howitwork , name='how_it_work'),
    path('sitemap', sitemap , name='site_map'),
    path('faq', faq , name='faq'),
    path('feedback', feedback , name='feedback'),
    path('feedback/send', feedbacks , name='feedbacks'),
    path('regions', regions , name='regions'),
    path('popular_search', popular_search , name='popular_search'),
    path('privacy', privacy , name='privacy'),
    path('terms', terms , name='terms'),
    path('contact/send', contact_views, name='contacts'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)