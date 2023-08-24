from django.contrib import admin
from .models import UploadedFile,Customer

@admin.register(Customer)
class RegistrationAdmin(admin.ModelAdmin):  
    list_display = ["id","user", "fullname", "mobileno","occupation"]

    
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ["id","user_id1","files1"]
