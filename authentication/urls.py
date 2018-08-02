from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views


#import social_network
#from social_network import views as socialview
#import search
#from search_app import views as search_view
#from django.contrib import admin
from .views import *

#import edite_data
#from edite_data import views as viewed

urlpatterns = [

	#url(r'^$', index),
	
	url(r'^index/proctorlogin/',views.login_proctor),
	url(r'^index/facultylogin/',views.login_faculty),
	url(r'^index/studentlogin/',views.login_student_member),
	
	url(r'^index/proctoreregistration/',views.add_proctor),
	url(r'^index/facultyregistration/',views.add_faculty),
	url(r'^index/studentregistration/',views.add_student_member),
	
	url(r'^index/',views.index),
	url(r'^student/',views.index_student),
	url(r'^proctor/',views.index_proctor),
	url(r'^faculty/',views.index_faculty),

	

	]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)