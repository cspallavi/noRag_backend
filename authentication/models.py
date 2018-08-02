from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Authority(models.Model):
	aid=models.AutoField(primary_key=True)
	aname=models.CharField(max_length=1000,null=False,blank=False)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	amobile_no = models.CharField(validators=[phone_regex], max_length=15, blank=False)
	apassword=models.CharField(max_length=1000,null=False,blank=False,default='')
	adesignation=models.CharField(max_length=50,null=False,blank=True,default='')
	aemail=models.EmailField(max_length=1000,null=False,blank=False)
	atype=models.CharField(max_length=100,default="")
	abranch=models.CharField(max_length=1000,default="",blank=True,null=False)
   	#faculties=models.ManyToManyField("self",default="Faculty",null=True)
   	#student_members=models.ManyToManyField("self",default="Student_member",null=True)

class Students(models.Model):
	sid=models.AutoField(primary_key=True)
	roll_no=models.CharField(max_length=1000,null=False,blank=False)
	email=models.EmailField(max_length=1000,null=False,blank=False)
	password=models.CharField(max_length=1000,null=False,blank=False)


class Student_details(models.Model):
	sid=models.ForeignKey(Students,on_delete=models.CASCADE)
	name=models.CharField(max_length=1000,null=False,blank=False)
	address=models.CharField(max_length=1000,null=False,blank=False)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	mobile_no = models.CharField(validators=[phone_regex], max_length=15, blank=False)
	g_mobile_no=models.CharField(validators=[phone_regex],max_length=15,blank=False)

class Complain(models.Model):
	cid=models.AutoField(primary_key=True)
	sid=models.ForeignKey(Students,on_delete=models.CASCADE)
	complain_txt=models.CharField(max_length=1000,null=False,blank=False)
	attachment=models.CharField(max_length=100,default='no')
	date=models.DateTimeField(auto_now=True,auto_now_add=False)
	status=models.CharField(max_length=100,default='not processed')
	share_status=models.CharField(max_length=100,default='no')

class Complain_Status(models.Model):
	cid=models.ForeignKey(Complain,on_delete=models.CASCADE)
	aid=models.ForeignKey(Authority,on_delete=models.CASCADE)
	voting=models.CharField(max_length=100,default="yes",blank=False,null=False)

class Notification_Authority(models.Model):
	nid=models.AutoField(primary_key=True)
	aid=models.ForeignKey(Authority,on_delete=models.CASCADE)
	notifcation=models.CharField(max_length=5000,blank=False,null=False,default='')
	date=models.DateTimeField(auto_now=True,auto_now_add=False)
	type_n=models.CharField(max_length=100,default='proctore',null=False,blank=False)

class Notification_Students(models.Model):
	nsid=models.AutoField(primary_key=True)
	sid=models.ForeignKey(Students,on_delete=models.CASCADE)
	notifcation=models.CharField(max_length=5000,blank=False,null=False,default='')
	date=models.DateTimeField(auto_now=True,auto_now_add=False)









