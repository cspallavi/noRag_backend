from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, render_to_response
from .models import *
from .forms import *
from passlib.hash import pbkdf2_sha256
from django.http import JsonResponse
from django.core.serializers import json
import json
import time
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail



def index(request):
	return render_to_response('index.html')
def index_student(request):
	#print("In the index student function")
	return render_to_response('student.html')
def index_proctor(request):
	return render_to_response('student.html')
def index_faculty(request):
	return render_to_response('student.html')



def login_proctor(request):
	if  request.method=="POST":
		#Login_Form = LoginForm(request.POST)
		#if Login_Form.is_valid():
		email=json.loads(request.body.decode("utf-8"))['email']
		password=json.loads(request.body.decode("utf-8"))['password']
		#hash_password = pbkdf2_sha256.encrypt(password,rounds=500000, salt_size=32)
		#print("The hashed password is"+str(hash_password))
		
		try:
			#print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
			#hash=pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(Login_Form.cleaned_data["password"])
			
			authority_object=Authority.objects.get(
				aemail=email,
				atype='Proctore'
				)


			#print("errorerrrrrrfrom django.shortcuts import render, render_to_responserrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
			#user_login=pbkdf2_sha256.using(rounds=200000, salt_size=32).verify(Login_Form.cleaned_data["password"], authority_object.password)
		except Exception as e:
			#messages.info(request, 'Login Failed')
			
			print("Login Failed "+str(e))
			
		dbpassword=authority_object.apassword

		print("The database password is "+str(dbpassword))

		if pbkdf2_sha256.verify(password,dbpassword):
			request.session["sessionid"]=authority_object.aid
			#return HttpResponseRedirect("/index/student/")
			#return render_to_response('student.html')
			#return redirect("/index/student/")
			return JsonResponse({'url':"/proctor/"},safe=False)
				
			
				

		

def login_faculty(request):
	if  request.method=="POST":
		#Login_Form = LoginForm(request.POST)
		#if Login_Form.is_valid():
		email=json.loads(request.body.decode("utf-8"))['email']
		password=json.loads(request.body.decode("utf-8"))['password']
		#hash_password = pbkdf2_sha256.encrypt(password,rounds=300000, salt_size=32)
		try:
			#print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
			#hash=pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(Login_Form.cleaned_data["password"])
			
			authority_object=Authority.objects.get(
				aemail=email,
				atype='faculty',
				)
			#print("errorerrrrrrfrom django.shortcuts import render, render_to_responserrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
			#user_login=pbkdf2_sha256.using(rounds=200000, salt_size=32).verify(Login_Form.cleaned_data["password"], authority_object.password)
		except Exception as e:
			#messages.info(request, 'Login Failed')
			print("Login Failed"+str(e))

		dbpassword=authority_object.apassword

		if pbkdf2_sha256.verify(password,dbpassword):
			request.session["sessionid"]=authority_object.aid
			return JsonResponse({'url':"/faculty/"},safe=False)
				

		

def login_student_member(request):
	if  request.method=="POST":
		#Login_Form = LoginForm(request.POST)
		#if Login_Form.is_valid():
		email=json.loads(request.body.decode("utf-8"))['email']
		password=json.loads(request.body.decode("utf-8"))['password']
		#hash_password = pbkdf2_sha256.encrypt(password,rounds=500000, salt_size=32)
			
		try:
			#print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
			#hash=pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(Login_Form.cleaned_data["password"])
			authority_object=Authority.objects.get(
				aemail=email,
				
				atype='student_member',
				)
			
		except Exception as e:
			#messages.info(request, 'Login Failed')
			print("Login Failed"+str(e))

		dbpassword=authority_object.apassword
		if pbkdf2_sha256.verify(password,dbpassword):
			request.session["sessionid"]=authority_object.aid
			return JsonResponse({'url':"/student/"},safe=False)
				





def student_registration(request):
	if request.method=="POST":
		roll_no=json.loads(request.body.decode("utf-8"))['roll_no']
		email=json.loads(request.body.decode("urf-8"))['email']
		
		random_string = get_random_string(length=32)
		password=pbkdf2_sha256.encrypt(
			random_string,
			rounds=100000, 
			salt_size=32,
			)

		try:
			student_object=Students(
				roll_no=roll_no,
				email=email,
				password=password,
				)
		except Exception as e:
			print("The excepion is "+str(e))
			student_object.save()

			return JsonResponse({'return_status':1},safe=False)







def student_login(request):
	if request.method=="POST":
		roll_no=json.loads(request.body.decode("utf-8"))['roll_no']
		password=json.loads(request.body.decode("utf-8"))['password']
		hash_password= pbkdf2_sha256.encrypt(password,rounds=100000,salt_size=32)
		try:
			student_object=Students.objects.get(roll_no=roll_no,password=hash_password)
			sessionuserid=student_object.sid
			request.session["sessionid"]=sessionuserid
		except Exception as e:
			print("The exception is"+str(e))

		return JsonResponse({'return_status':2,'sessionid':sessionuserid},safe=False)

		



def add_proctor(request):
	if request.method=="POST":
		
		if not request.session.get('sessionid',None):
			return HttpResponse("Login required")
		
		sessionid=request.session['sessionid']
		print("The session id is "+str(sessionid))
		name=json.loads(request.body.decode('utf-8'))["name"]
		random_string = get_random_string(length=32)
		#password=json.loads(request.body.decode('utf-8'))["password"]

		email=json.loads(request.body.decode('utf-8'))["email"]
		lemail=[]
		lemail.append(email)
		send_mail('No Rag', 
			'This is your password -'+random_string+'Please Change after you login', 
			settings.EMAIL_HOST_USER,
			lemail, 
			fail_silently=False
			)
		mobile_no=json.loads(request.body.decode('utf-8'))["phone"]
		designation=json.loads(request.body.decode('utf-8'))["designation"]
		branch=json.loads(request.body.decode('utf-8'))['branch']
		hash_password = pbkdf2_sha256.encrypt(random_string,rounds=500000, salt_size=32)
		print ("THE SESSION ID IS"+str(sessionid))        
		try:
			entry_proctor=Authority(aname=name,
				amobile_no=mobile_no,
				apassword=hash_password,
				adesignation=designation,
				aemail=email,
				atype='Proctore',
				abranch=branch
				)
		except Exception as e:
			print ("The error is"+str(e))
		entry_proctor.save()
		return HttpResponse()
        


def add_faculty(request):
	if request.method=='POST':
		if not request.session.get('sessionid',None):
			return HttpResponse("Login required")
		sessionid=request.session['sessionid']
		name=json.loads(request.body.decode('utf-8'))["name"]
		random_string = get_random_string(length=32)
		

		email=json.loads(request.body.decode('utf-8'))["email"]
		lemail=[]
		lemail.append(email)
		send_mail('No Rag', 
			'This is your password -'+random_string+'Please Change after you login', 
			settings.EMAIL_HOST_USER,
			lemail, 
			fail_silently=False
			)
		branch=json.loads(request.body.decode('utf-8'))['branch']
		mobile_no=json.loads(request.body.decode('utf-8'))["phone"]
		designation=json.loads(request.body.decode('utf-8'))["designation"]
		hash_password = pbkdf2_sha256.encrypt(random_string,rounds=300000, salt_size=32)
		print ("THE SESSION ID IS"+str(sessionid))
		try:
			entry_faculty=Authority(aname=name,amobile_no=mobile_no,apassword=hash_password,adesignation=designation,aemail=email,atype='faculty',abranch=branch)
		except Exception as e:
			print ("The error is"+str(e))
		
		entry_faculty.save()
		return HttpResponse() 
			
			



def add_student_member(request):
	if request.method=="POST":
		if not request.session.get('sessionid',None):
			return HttpResponse("Login required")
		sessionid=request.session['sessionid']
		name=json.loads(request.body.decode('utf-8'))["name"]
		random_string = get_random_string(length=32)
		
		email=json.loads(request.body.decode('utf-8'))["email"]
		lemail=[]
		lemail.append(email)
		send_mail('No Rag', 
			'This is your password -'+random_string+'Please Change after you login', 
			settings.EMAIL_HOST_USER,
			lemail, 
			fail_silently=False
			)
		mobile_no=json.loads(request.body.decode('utf-8'))["phone"]
		branch=json.loads(request.body.decode('utf-8'))['branch']
		designation=json.loads(request.body.decode('utf-8'))["designation"]
		hash_password = pbkdf2_sha256.encrypt(random_string,rounds=200000, salt_size=32)
		print ("THE SESSION ID IS"+str(sessionid))
		try:
			entry_student_member=Authority(aname=name,amobile_no=mobile_no,apassword=hash_password,adesignation=designation,aemail=email,atype='student_member',abranch=branch)
		except Exception as e:
			print ("The error is"+str(e))
		entry_student_member.save()
		return HttpResponse()

def change_password(request):
	if request.method=="POST":
		if not request.session.get('sessionid',None):
			return HttpResponse("Login required")
		sessionid=request.session['sessionid']
		oldpassword=json.loads(request.body.decode("utf-8"))['oldpassword']
		newpassword=json.loads(request.body.decode("utf-8"))['newpassword']
		cnewpassword=json.loads(request.body.decode("utf-8"))['cnewpassword']

		try:
			authority_object=Authority.objects.get(aid=sessionid,apassword=oldpassword)
		except Exception as e:
			print("The exception is"+str(e))
		if newpassword!=cnewpassword:
			return JsonResponse({'message':"Password Didnt Match"},safe=False)
		else:
			authority_object.apassword=newpassword
			authority_object.save()

		return JsonResponse({'message':"Password Changed Successfully"})

def forgot_password(request):
	if request.method=="POST":
		email=json.loads(request.body.decode('utf-8'))['email']
		try:
			authority_object=Authority.objects.get(email=email)
		except Exception as e:
			print("The exception is "+str(e))



		if authority_object:

			random_string = get_random_string(length=32)
		
			lemail=[]
			lemail.append(email)
			send_mail('No Rag',
				'This is your password -'+random_string+'Please Change after you login',
				settings.EMAIL_HOST_USER,
				lemail,
				fail_silently=False
				)

			authority_type=authority_object.atype
			
			if authority_type=='Proctore':
				hash_password = pbkdf2_sha256.encrypt(random_string,rounds=500000, salt_size=32)
			elif authority_type=='faculty':
				hash_password=pbkdf2_sha256.encrypt(random_string,rounds=300000, salt_size=32)
			elif authority_type=='student_member':
				hash_password = pbkdf2_sha256.encrypt(random_string,rounds=200000, salt_size=32)

			authority_object.apassword=hash_password
			authority_object.save()


def change_settings(request):
	if request.method=='POST':
		if not request.session.get('sessionid',None):
			return HttpResponse("Login required")
		sessionid=request.session('sessionid',None)
		name=json.loads(request.body.decode('utf-8'))['name']
		email=json.loads(request.body.decode('utf-8'))['email']
		phone=json.loads(request.body.decode('utf-8'))['phone']
		branch=json.loads(request.body.decode('utf-8'))['branch']
		designation=json.loads(request.body.decode('utf-8'))['designation']

		try:
			authority_object=Authority.objects.get(aid=sessionid)
		except Exception as e:
			print("The exception is "+str(e))

		if name is not None:
			authority_object.aname=name
		if email is not None:
			authority_object.aemail=email
		if phone is not None:
			authority_object.aphone=phone
		if branch is not None:
			authority_object.branch=branch
		if designation is not None:
			authority_object.designation=designation

		authority_object.save()
		try:
			new_authority_object=Authority.objects.get(aid=sessionid)
		except Exception as e:
			print("The exception is "+str(e))

		newemail=new_authority_object.aemail
		newname=new_authority_object.aname
		newphone=new_authority_object.aphone
		newbranch=new_authority_object.abranch
		newdesignation=new_authority_object.designation

		context_authority={}
		context_authority['email']=newemail
		context_authority['name']=newname
		context_authority['phone']=newphone
		context_authority['branch']=newbranch
		context_authority['designation']=newdesignation

		print("The context authority is"+str(context_authority))

		return JsonResponse(context_authority,safe=False)





#def change_about(request):

def show_all_authority(request):
	if request.method=='POST':
		if not request.session.get('sessionid',None):
			return HttpResponse("Login required")
		sessionid=request.session('sessionid',None)
		try:
			authority_object=Authority.objects.all()
		except Exception as e:
			print("The exception is"+str(e))
		
		context_authority={}
		context_authority_list=[]
		for authority in authority_object:
			context_authority['name']=authority.aname
			context_authority['phone']=authority.aphone
			context_authority['email']=authority.aemail
			context_authority['branch']=authority.abranch
			context_authority['designation']=authority.adesignation
			print("This is context "+str(context_authority))
			context_authority_list.append(context_authority)

		print("The context authority list is"+str(context_authority_list))

		return JsonResponse(context_authority_list,safe=False)


def particular_authority(request):
	if request.method=='POST':
		if not request.session.get('sessionid',None):
			return HttpResponse("Login required")
		sessionid=request.session('sessionid',None)
		atype=json.loads(request.body.decode('utf-8'))['atype']
		try:
			authority_object=Authority.objects.filter(atype=atype)
		except Exception as e:
			print("The exception is"+str(e))
		
		context_authority={}
		context_authority_list=[]
		for authority in authority_object:
			context_authority['name']=authority.aname
			context_authority['phone']=authority.aphone
			context_authority['email']=authority.aemail
			context_authority['branch']=authority.abranch
			context_authority['designation']=authority.adesignation
			print("This is context "+str(context_authority))
			context_authority_list.append(context_authority)

		print("The context authority list is"+str(context_authority_list))

		return JsonResponse(context_authority_list,safe=False)

def show_details(request):
	if request.method=='POST':
		if not request.session.get('sessionid',None):
			return HttpResponse("Login required")
		sessionid=request.session('sessionid',None)
		#atype=json.loads(request.body.decode('utf-8'))['atype']
		try:
			authority_object=Authority.objects.get(aid=sessionid)
		except Exception as e:
			print("The exception is"+str(e))
		
		context_authority={}
		
		if authority_object:
			context_authority['name']=authority.aname
			context_authority['phone']=authority.aphone
			context_authority['email']=authority.aemail
			context_authority['branch']=authority.abranch
			context_authority['designation']=authority.adesignation
			print("This is context "+str(context_authority))
			
		return JsonResponse(context_authority,safe=False)






