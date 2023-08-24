from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_view 

from django.urls import path
from TCPLapp import views
from django.conf.urls.static import static

from TCPLapp.forms import LoginForm




urlpatterns = [
# path("admin/", admin.site.urls),
path('', auth_view.LoginView.as_view(template_name="TCPLapp/login.html",authentication_form=LoginForm),name="login"),

path('registration/', views.CustomerRegistrationForm.as_view(),name="customerregistration"),
  
path('profile/', views.ProfileView.as_view(), name='profile'),

path('basemap/', views.basemap, name='basemap'),
   
path('user_details/', views.user_details, name='user_details'),
     
#    path('user/', views.user,name='user'),
   
#    path('profile/', views.ProfileView.as_view(), name='profile'),
   
   
   
    
    
    #path('main/', views.main,name='main'),
    
    
    
    # path('user_details/<int:id>/', views.user_details,name='user_details'),
    
path('logout/',views.logout,name='logout'),
    
    # #path('coordinates/',views.coordinates,name='coordinates'),
    
path('index/', views.index,name='index'),
    
path('zoneDetail/', views.zoneDetail,name='zoneDetail'),

path('planSurvey/', views.planSurvey,name='planSurvey'),
    
path('mapCalculator/', views.mapCalculator,name='mapCalculator'),
    
path('upload_file_page/', views.upload_file_page, name='upload_file_page'),
   
    path('upload_file/', views.upload_file, name='upload_file'),
    
    
    
    
    
    
    # path('autocomplete/', views.autocomplete, name='autocomplete'),
    
    # path('searchOnClick/', views.searchOnClick, name='searchOnClick'),
    
    # path('Out_table/', views.Out_table, name='Out_table'),
    
    # path('save-location/', views.save_location, name='save_location'),
    
    # path('get-locations/', views.get_locations, name='get_locations'),
    
    # path('delete-location/', views.delete_location, name='delete_location'),
    
    # path('fetch_searchdata/<int:id>/',views.fetch_searchdata, name='fetch_searchdata')
   
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
