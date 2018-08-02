from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#import social_network
#from social_network import views as socialview
#import search
#from search_app import views as search_view
#from django.contrib import admin
from .views import *
#import edite_data
#from edite_data import views as viewed

urlpatterns = [

	#url(r'^student/',index_student),

	
	#url(r'^accountverification/',verify_account),
	]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	