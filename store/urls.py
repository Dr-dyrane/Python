from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings

from django.views.generic import TemplateView
from django_filters.views import FilterView
from .filters import ProductFilter

urlpatterns = [
    path ('', views.store, name = "store"),
    path ('cart/', views.cart, name = "cart"),
    path ('account/', views.account, name = "account"),
    
    path ('edit_account/<str:pk>', views.edit_account, name = "edit_account"),
    path ('edit_account/update_account/<str:pk>', views.update_account, name = "update_account"),
    
    path ('guest_account/', views.guest_account, name = "guest_account"),
    path ('checkout/', views.checkout, name = "checkout"),
    path ('login/', views.login, name = "login"),
    path ('register/', views.register, name = "register"),
    path ('logout/', views.logout_view, name = "logout"),

    path ('update_item/', views.updateItem, name = 'update_item'),
    path ('product/<str:pk>', views.product_page, name = 'product'),
    path ('drug_class/<str:pk>', views.drug_class, name='drug_class'),
    path ("favicon.ico",RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),),
    path('search/', views.search, name='search'),
    path ('checkout/process_order/', views.processOrder,name ='process_order'),
]


