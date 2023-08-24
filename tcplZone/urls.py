from django.contrib import admin
from django.urls import path, include
from TCPLapp import views
  




urlpatterns = [
    path("admin/", admin.site.urls),
    
    path('', include('TCPLapp.urls')),
    # path('',views.login,name='login'),
]