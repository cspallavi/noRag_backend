from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Authority)
admin.site.register(Students)
admin.site.register(Student_details)
admin.site.register(Complain)
admin.site.register(Complain_Status)
admin.site.register(Notification_Authority)
admin.site.register(Notification_Students)

