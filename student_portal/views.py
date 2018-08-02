from django.shortcuts import render
from django.shortcuts import render_to_response


# Create your views here.
def index_student(request):
	 return render_to_response('student.html')