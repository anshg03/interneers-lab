from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',views.hello_world,name='hello_world'),
    path('product/',include('product.urls'))
]
