from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
import Todoapp
from Todoapp.models import Todomodel



# Create your views here.
def home(request):
	no_of_items = Todomodel.objects.latest('id').id
	no_of_users = User.objects.latest('id').id
	print no_of_items , no_of_users
	return render(request,'accounts/home.html',{'users':no_of_users,'items':no_of_items})

def signup(request):
	if request.method == 'POST':
		if request.POST['password1']==request.POST['password2']:
			try:
				user=User.objects.get(username = request.POST['username'])
				return render(request,'accounts/signup.html',{'error':'Employee ID already exists'})
			except User.DoesNotExist:
				user=User.objects.create_user(request.POST["username"], password=request.POST["password1"])
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				login(request, user)
				return redirect('todoapp:register')
		else:
			return render(request,'accounts/signup.html',{'error':'Passwords don\'t match'});
	else:
		return render(request,'accounts/signup.html');

def loginview(request):
	if request.method =='POST':
		user = authenticate(username=request.POST.get('username', None),password=request.POST.get('password', None))
		if user is not None:
			login(request,user)
			print 'next is',request.POST.get('next',None)
			if request.POST.get('next',None) is not None:
				return redirect(request.POST['next'])
			#return render(request,'accounts/login.html',{'info':'Logged in!!'});
			#return HttpResponseRedirect('Todoapp/register.html',{'info':'Logged in!!'});
			return redirect('todoapp:register')
			
		else:
			return render(request,'accounts/login.html',{'info':'incorrect username password'});
	else:
		return render(request,'accounts/login.html');


def logoutview(request):
	if request.method =='POST':
		logout(request)
		return render(request,'accounts/logout.html');
	return render(request,'accounts/login.html',{'info':'Not yet!!'});