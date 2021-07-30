from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.get_all_products, name='all_products'),
    path('releases/<int:pk>', views.get_releases, name="releases"),
    path('testresults/', views.get_testresults, name='testresults'),
    
]