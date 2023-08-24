
import os
from django.conf import settings
from django.shortcuts import render,HttpResponse,redirect, get_object_or_404 ,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from .models import Customer, Location, UploadedFile, elements, Revenue1,FinalPlu

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import UploadedFile
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.serializers.geojson import Serializer as GeoJSONSerializer
from django.contrib.gis.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
import json
import geopandas as gpd
from pyproj import CRS
import requests
from django.contrib import messages
from .forms import CustomerProfileForms,CustomerRegiForm

#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
from io import BytesIO
import io
from django.contrib.auth import authenticate
# from .forms import uploadFileForm

###################### new code ##########################
#_____________ Customer Registration _____________________________

class CustomerRegistrationForm(View):
    def get(self,request):
        form=CustomerRegiForm()
        
        return render(request,'TCPLapp/customerregistration.html',{"form":form})
    
    def post(self,request):
        form=CustomerRegiForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'TCPLapp/customerregistration.html',{"form":form})


#_____________ profile _____________________________
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForms()
        return render(request,'TCPLapp/profile.html',{"form":form,"active":"btn-primary"})
    
    def post(self,request):
        form=CustomerProfileForms(request.POST)
        if form.is_valid():
            usr=request.user
            fullname=form.cleaned_data["fullname"]
            
            mobileno=form.cleaned_data["mobileno"]
            
            dob=form.cleaned_data["dob"]
            
            address=form.cleaned_data['address']
            
            occupation=form.cleaned_data["occupation"]

            industry = form.cleaned_data["industry"]
            
            reg=Customer(user=usr,fullname=fullname,mobileno=mobileno,occupation=occupation,dob=dob,address=address, industry=industry)
            
            reg.save()
            messages.success(request,"Congratulations !! Profile Updated Successfully")
       
            return render(request, 'TCPLapp/profile.html',{"form":form,"active":"btn-primary"})

#_______________user_details______________________
@login_required
def user_details(request):
    add=Customer.objects.filter(user=request.user) #This is to get the current user,it solve the problem like to store user in login as a session.
    
    return render(request, 'TCPLapp/user_details.html',{"add":add,"active":"btn-primary"})
    


########################################################



# # registration______________________________________________________________________
# def registration(request):
#     # return render(request,'TCPLapp/registration.html')
#     if request.method=='POST':
#         fullname=request.POST.get('fullname')
#         username=request.POST.get('username')
#         mobileno=request.POST.get('mobileno')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         occupation=request.POST.get('occupation')
        
#         Register_details=Registration.objects.create(fullname=fullname,username=username,mobileno=mobileno,email=email,password=password,occupation=occupation)
        
#         Register_details.save()
#         context={'data':'Register_details'}
        
#     return render(request, 'TCPLapp/registration.html')
                 
#     # else: 
        
#     #     return render(request, 'TCPLapp/login.html')
    
#     # return render(request,"TCPLapp/registration.html")
    
    
    
# _______________________________________________    
# def loginform(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         try:
#             user = Registration.objects.get(username=username)
#             if check_password(password, user.password):
#                 # Authentication successful, create a session for the user
#                 request.session['user_id'] = user.id
#                 return redirect("basemap")
#         except Registration.DoesNotExist:
#             pass

#         # Authentication failed
#         return redirect("login")
#     else:
#         return render(request, 'TCPLapp/login.html')
    

# def loginform(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)

#         if user is None:
#             return redirect("login")
#         else:
#             login(request, user)
#             return redirect("profile")
#     else:
#         return render(request, 'TCPLapp/login.html')

# @login_required
# def profile(request):
#     profile_obj=User.objects.filter(username=request.user)#This is to get the current user,it solve the problem like to store user in login as a session.
    
#     # print(profile_obj.fullname)
    
    
#     return render(request, 'TCPLapp/profile.html',{"profile_obj":profile_obj,"active":"btn-primary"})

def basemap(request):
    return render(request, 'TCPLapp/basemap.html')


def index(request):
    return render(request, 'TCPLapp/index.html')

def logout(request):
    # Do not use "return render" here
    # return render(request, 'TCPLapp/login.html')
    return redirect("login")

def zoneDetail(request):
      return render(request, 'TCPLapp/zoneDetail.html')

def planSurvey(request):
      return render(request, 'TCPLapp/planSurvey.html')
  
  
def mapCalculator(request):
      return render(request, 'TCPLapp/mapCalculator.html')
  
  
def upload_file_page(request):
      return render(request, 'TCPLapp/upload_file.html')
    

# def upload_file(request):
#     from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage

@login_required
def upload_file_page(request):
    return render(request, 'TCPLapp/upload_file.html')

@login_required
# @staticmethod   
def upload_file(request):
        if request.method == 'POST' and 'file' in request.FILES:
            # Check if the user is authenticated
            if request.user.is_authenticated:
                uploaded_file = request.FILES['file']
                allowed_extensions = ['.jpg', '.jpeg', '.pdf', '.tif', '.tiff']

                if any(uploaded_file.name.lower().endswith(ext) for ext in allowed_extensions):
                    # Save the uploaded file using the model
                    uploaded_file_instance = UploadedFile(files1=uploaded_file, user_id1=request.user)
                    uploaded_file_instance.save()

                    message = 'File uploaded successfully!'
                else:
                    message = 'Invalid file format. Allowed formats: JPG, PDF, TIFF.'
            else:
                message = 'User is not authenticated.'
        else:
            message = ''
        return render(request, 'TCPLapp/upload_file.html', {'message': message})


# @login_required
# def upload_file(request):
#     if request.method == 'POST' and 'file' in request.FILES:
#     #    if request.user.is_authenticated(): 
#         uploaded_file = request.FILES['file']
#         allowed_extensions = ['.jpg', '.jpeg', '.pdf', '.tif', '.tiff']
        
#         if any(uploaded_file.name.lower().endswith(ext) for ext in allowed_extensions):
#             # Save the uploaded file using the model
#             uploaded_file_instance = UploadedFile(files1=uploaded_file)
#             uploaded_file_instance.save()
            
#             message = 'File uploaded successfully!'
#         else:
#             message = 'Invalid file format. Allowed formats: JPG, PDF, TIFF.'
#     else:
#         message = ''
#     return render(request, 'TCPLapp/upload_file.html', {'message': message})


# @login_required
# def upload_file(request):
#     if request.method == 'POST' and 'file' in request.FILES:
#         uploaded_file = request.FILES['file']
#         allowed_extensions = ['.jpg', '.jpeg', '.pdf', '.tif', '.tiff']
#         if any(uploaded_file.name.lower().endswith(ext) for ext in allowed_extensions):
            
#             # fs = FileSystemStorage()
            
#             # fs.save(uploaded_file.name, uploaded_file)
            
#             # Create an instance of FileSystemStorage using MEDIA_ROOT
#             media_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

#             # Specify the subfolder where you want to save the file
#             subfolder_name = 'file'
#             file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, subfolder_name))

#             # Process the file upload and save it in the subfolder
#             uploaded_file = request.FILES['file']
#             file_storage.save(uploaded_file.name, uploaded_file)
                    
#             message = 'File uploaded successfully!'
#         else:
#             message = 'Invalid file format. Allowed formats: JPG, PDF, TIFF.'
#     else:
#         message = ''
#     return render(request, 'TCPLapp/upload_file.html', {'message': message})
#     # return redirect("upload_file_page")




# def login(request):
#      if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request)
#             # Redirect to a success page or wherever you want
#             return redirect('user')
#         else:
#             # Handle invalid login
#             error_message = "Invalid login credentials. Please try again."
#             return render(request, 'TCPLapp/login.html', {'error_message': error_message})
    
#      return render(request, 'TCPLapp/login.html')  # Render your login page template

    
# @method_decorator(login_required,name='dispatch')
# class ProfileView(View):
#     def get(self,request):
#         form=CustomerProfileForms()
#         return render(request,'TCPLapp/profile.html',{"form":form,"active":"btn-primary"})
    

 
# # login______________________________________________________________________
# @login_required
# @csrf_exempt
# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Use the authenticate function to validate the user's credentials
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             # Use the login function to log in the user
#             login(request, user)
            
#             if username == 'admin_host' and password == 'admin@123':
#                 # Only retrieve data if it's an admin user
#                 data1 = Registration.objects.all()
#                 count = data1.count()
#                 context = {'data1': data1, 'count': count}
#                 return render(request, 'TCPLapp/admin123.html', context)
#             else:
#                 return render(request, 'TCPLapp/user.html')  # Render a user-specific template
            
#         else:
#             # Handle invalid login credentials
#             return render(request, 'TCPLapp/login.html', {'error': 'Invalid login credentials'})

#     return render(request, 'TCPLapp/login.html')














































































































# #main ______________________________________________________________________
# @login_required(login_url='login')
# # def main(request):

   
# #     # user = request.user
  
# #     # if request.method == 'POST':
       
# #         # name = request.POST.get('name')
# #         # latitude = request.POST.get('lat')
# #         # longitude = request.POST.get('lng')
# #         # new_bookmark = BookMarks.objects.create(name=name, latitude=latitude, longitude=longitude)
# #         # new_bookmark.save()
# #         return redirect('main')
# #     # return render(request, "TCPLapp/main.html", {'bookmarks': bookmarks_from_database})


# def main(request):
#    return render(request,"TCPLapp/main.html") 




# # registration______________________________________________________________________
# def registration(request):
    
#     if request.method=='POST':
        
#         uname=request.POST.get('username')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')
        
#         if pass1!=pass2:
#             return render(request, 'TCPLapp/registration.html', {'error': 'Invalid login credentials'})
                 
                
        
#         else:
#             my_user=User.objects.create_user(uname,email,pass1)
#             my_user.save()
#         return redirect('login')
#     return render(request,"TCPLapp/registration.html")


# # login______________________________________________________________________
# @login_required
# @csrf_exempt
# def loginPage(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username,password=pass1)
#         if user is not None:
#             login(request,user)
            
#             if username=='admin_host' and pass1=='admin@123':
#                 data1=User.objects.all()
#                 count=data1.count()                                                                               
#                 #print(count,'aaaaaaaaaaaaaaaaaaa')
#                 context={'data1':data1,'count':count}
#                 #print(context,'aaaaaaaaaaa')
            
#                 return render(request,'TCPLapp/admin123.html',context)
            
#             elif  username=='mainadmin' and pass1=='1234':
               
#                 return render(request,'TCPLapp/mainadmin.html')
           
                
            
#             else:
#                 return redirect('index')
            
#         else:
#             # Handle invalid login credentials
#             return render(request, 'TCPLapp/login.html', {'error': 'Invalid login credentials'})
        
#     return render(request,"TCPLapp/login.html")


# @login_required
# def user_details(request,id):
#     data2=Location.objects.filter(user_id=id)
    
    
#     locations=[]
#     # locations1=[]
#     for i in data2:
#         user=i.user_id
#         print()
#         name=i.name        
#         latitude=i.latitude
#         longitude=i.longitude
        
        
#         location_data = {'name': name, 'latitude': latitude, 'longitude': longitude,'user':user}
        
        
#         #print(location_data,'aaaaaaaaaaaaaaaa')
#         locations.append(location_data)
        
        
#         data1= villagetalukadata.objects.filter(user_id=id)
#     #print(data1,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
#     # for i in data1:
#     #     print(i.user_id,'aaaabollllll')
#     #     print(i.village,'aabbcc')
#     #     print(i.taluka,'wwwwwwwwwwwww')
#     #     print(i.gut,'qqqqqqqqqqqqqqqqqqqqq')
        
    
#     search_datas=[]
#     for i in data1:
       
#         user=i.user_id
#         village=i.village
#         taluka=i.taluka
#         gut=i.gut
        
#         search_data = {'village': village, 'taluka': taluka,'gut':gut,'user':user}
#         search_datas.append(search_data)
#         #print(search_datas,'aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        
        
        
#     # return render(request, 'TCPLapp/register_details.html', {'locations': locations,"user":location_data})
#     return render(request,"TCPLapp/searchdata.html",{'locations': locations,"user":location_data,'search_datas':search_datas})  



# # def fetch_searchdata(request,id):
    
# #     data1= villagetalukadata.objects.filter(user_id=id)
# #     #print(data1,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
# #     # for i in data1:
# #     #     print(i.user_id,'aaaabollllll')
# #     #     print(i.village,'aabbcc')
# #     #     print(i.taluka,'wwwwwwwwwwwww')
# #     #     print(i.gut,'qqqqqqqqqqqqqqqqqqqqq')
        
    
# #     search_datas=[]
# #     for i in data1:
       
# #         user=i.user_id
# #         village=i.village
# #         taluka=i.taluka
# #         gut=i.gut
        
# #         search_data = {'village': village, 'taluka': taluka,'gut':gut,'user':user}
# #         search_datas.append(search_data)
# #         #print(search_datas,'aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        
# #     return render(request,"TCPLapp/searchdata.html",{'search_datas':search_datas})  
    

# def Out_table(request):
    
#     response = request.GET.get("selected_value").split(",")
#     villageName, talukaName, gutNumber = response[0], response[1], response[2:]
#     gutnumber2=response[2:]
    
    
#     products1 = Revenue1.objects.filter(taluka=talukaName, village_name_revenue=villageName, gut_number=str(gutNumber[0]))
#     intersection_query = Q(geom__intersects=products1[0].geom)
    
    
#     for product in products1[1:]:
#         intersection_query |= Q(geom__intersects=product.geom)
#     plu = FinalPlu.objects.filter(intersection_query)
#     data = []
#     for Iplu in plu:
#         intersection_area = Iplu.geom.intersection(products1[0].geom).area
      
#         data.append(Iplu.broad_lu)
#         data.append(intersection_area)
        
#     data1 = {
        
#         "Village_Name": villageName,
#         "Taluka_Name": talukaName,
#         "Gut_Number": gutNumber,
#         "selected_values": data
#     }
    
    
    
#     search_history = villagetalukadata.objects.create(
#         user=request.user,
#         village=villageName,
#         taluka=talukaName,
#         gut=str(gutNumber[0])
#     )
#     search_history.save()

#     #print(search_history,'aaaaaaaaaaaaaaaaaaaaa')
   
    
#     return JsonResponse(data1,safe=False)
   
    

 
 
# #logout ______________________________________________________________________
# def LogoutPage(request):
#     logout(request)
#     return redirect('login')


# # index__________________________________________________

# @login_required(login_url='login')
# def index(request):
  

#     return render(request, "TCPLapp/index.html")

# # search_button________________________________

# def autocomplete(request):
#     term = request.GET.get('term')
    
#     if term is not None:
#         products = elements.objects.filter(village_name_revenue__istartswith=term).values_list('village_name_revenue','taluka')
#         products_list1 = list(set(products))
#         products_list = [','.join(t) for t in products_list1]
        
        
#     return JsonResponse(products_list, safe=False)


# def convert_To_Geojson(products1):
#     for instance in  products1:
#         coordinates_list = []
#         geom_geojson = GEOSGeometry(json.dumps({"type": "MultiPolygon", "coordinates": [instance.geom.coords[0]]}))
#         feature = {
#         "type": "Feature",
#         "geometry": json.loads(geom_geojson.geojson),
#         "properties": {
#             "village_name_revenue": instance.village_name_revenue,
#             "taluka": instance.taluka,
#                         } }
#         coordinates_list.append(feature)
#         geojson_data = {
#                     "type": "FeatureCollection",
#                     "features": coordinates_list
#                             }
  
#     return geojson_data

# def searchOnClick(request):
#     response = request.GET.get("selected_value").split(",")
#     villageName, talukaName, gutNumber = response[0],response[1],response[2:]
#     products1 = Revenue1.objects.filter(taluka=talukaName,  village_name_revenue=villageName, gut_number= str(gutNumber[0]))
#     geojson_gut = convert_To_Geojson(products1)
    
#     intersection_query = Q(geom__intersects=products1[0].geom)
#     for product in products1[1:]:
#         intersection_query |= Q(geom__intersects=product.geom)
#     plu = FinalPlu.objects.filter(intersection_query)
#     for Iplu in plu:
#         intersection_area = Iplu.geom.intersection(products1[0].geom).area
#     # You can adjust the calculation based on your use case and data model
#         # print(f"PLU ID: {Iplu.broad_lu}, Iplu.shape_area : {Iplu.shape_area},Intersection Area: {intersection_area}")
       
#     # #  layer intersection of plu and gut number
#     # intersected_geometries = []
#     # for Irevenue in products1:
#     #     for Iplu in plu:
#     #         intersection = Irevenue.geom.intersection(Iplu.geom)
#     #         if intersection:
#     #             intersected_geometries.append(intersection)
#     #         else:
#     # print(intersected_geometries,"_______________________________________")
#     # for d in intersected_geometries:
#     #     print(d,"{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}")
    
#     # intersection_json = convert_To_Geojson(intersected_geometries)
#     # print(intersection_json)
   
#     return JsonResponse(geojson_gut, safe=False)



     
     
# # Save BookMarks_____________________________

# @csrf_exempt
# @login_required
# def save_location(request):
#     if request.method == 'POST':
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')
#         name = request.POST.get('name')
#         username = request.POST.get('username')

#         location = Location(user=request.user, name=name,
#                             latitude=latitude, longitude=longitude)
#         location.save()

#         return JsonResponse({'message': 'Location saved successfully.'})
#     else:
#         return JsonResponse({'message': 'Invalid request method.'})


# def get_locations(request):
#     locations = Location.objects.filter(user=request.user)
#     data = {
#         'locations': list(locations.values('id','name', 'latitude', 'longitude'))
#     }
#     return JsonResponse(data)

# #delete_location
# @csrf_exempt
# @login_required
# def delete_location(request):
#     if request.method == 'POST':
#         location_id = request.POST.get('locationId')
#         try:
#             location = Location.objects.get(id=location_id)
#             if location.user == request.user:
#                 location.delete()
#                 return JsonResponse({'message': 'Location deleted successfully.'})
#             else:
#                 return JsonResponse({'message': 'Unauthorized access.'}, status=401)
#         except Location.DoesNotExist:
#             return JsonResponse({'message': 'Location not found.'}, status=404)
#     else:
#         return JsonResponse({'message': 'Invalid request method.'}, status=400)
 
 

    
