from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
import Todoapp
from Todoapp.models import Todomodel
from django.contrib import messages



# Create your views here.
def home(request):
	no_of_items = Todomodel.objects.latest('id').id
	no_of_users = User.objects.latest('id').id
	print ('no_of_items-->{}',format(no_of_users))
	return render(request,'accounts/home.html',{'users':no_of_users,'items':no_of_items})

def signup(request):
	if request.method == 'POST':
		if request.POST['password1']==request.POST['password2']:
			try:
				user=User.objects.get(username = request.POST['username'])
				messages.warning(request,"Username already exists")
				return render(request,'accounts/signup.html')
			except User.DoesNotExist:
				user=User.objects.create_user(request.POST["username"], password=request.POST["password1"])
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				login(request, user)
				return redirect('todoapp:register')
		else:
			messages.warning(request,"Passwords do not match")
			return render(request,'accounts/signup.html');
	else:
		return render(request,'accounts/signup.html');

def loginview(request):
	if request.method =='POST':
		user = authenticate(username=request.POST.get('username', None),password=request.POST.get('password', None))
		if user is not None:
			login(request,user)
			print ('next is {}',format(request.POST.get('next',None)))
			if request.POST.get('next',None) is not None:
				return redirect(request.POST['next'])
			return redirect('todoapp:register')
		else:
			messages.warning(request, 'Incorrect username password')
			return render(request,'accounts/login.html');
	else:
		return render(request,'accounts/login.html');


def logoutview(request):
	if request.method =='POST':
		logout(request)
		return render(request,'accounts/logout.html');
	return render(request,'accounts/login.html',{'info':'Not yet!!'});


def reset_password(request):	
	if request.method == 'POST':
		if request.POST['password1']==request.POST['password2']:
			try:
				user=User.objects.get(username = request.POST['username'])
				user.set_password(request.POST['password1'])
				user.save()
				messages.success(request,"Password changed")
				return redirect('accounts:login')
			except User.DoesNotExist:
				messages.warning(request,"User Does Not Exist")
				return render(request,'accounts/reset_password.html')
			
		else:
			messages.warning(request,"Passwords do not match")
			return render(request,'accounts/reset_password.html');
	else:
		return render(request,'accounts/reset_password.html');