from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from models import Todomodel
import datetime
from datetime import date,timedelta
from forms import Todoform,Loginform
from django.shortcuts import get_object_or_404
# Create your views here.

def login(request):
	if request.method == 'POST':
		loginform = Loginform(request.POST)
		if loginform.is_valid():
			print 'login form is valid'
			#todoform = Todoform()
			#return render(request,'Todoapp/register.html',{'todoform':todoform})
	else:
		loginform = Loginform()
		return render(request,'Todoapp/login.html',{'loginform':loginform})

def register(request):
	if request.method == 'POST': # for a form with data in it
		todoform = Todoform(request.POST)
		if todoform.is_valid():
			#print 'form is valid'
			item = todoform.save(commit = False)
			item.save()
			#print 'save the item'
	todoform = Todoform() #just for displaying empty form
	list = Todomodel.objects.filter(date=datetime.date.today())
	pending_list = Todomodel.objects.filter(status='1')
	return render (request,'Todoapp/register.html',{'todoform':todoform,'list':list,'pending_list':pending_list})	
	
def list(request):
	#print 'came to list'
	list = Todomodel.objects.all().order_by('-date')	
	return render(request,'Todoapp/list.html',{'list':list})

def details(request,item_id):
	item = get_object_or_404(Todomodel,id=item_id)
	#item  = Todomodel.objects.get(id = item_id)
	return render(request,'Todoapp/details.html',{'item':item})

def edit(request,item_id=None):	
	#item = get_object_or_404(Todomodel,id=item_id)
	item = Todomodel.objects.get(pk = item_id)
	#print 'item is --->', item	
	todoform = Todoform(request.POST or None,instance = item)
	context = { 'date' : item.date,
				'description' : item.description,
				#'done' : item.done,
				#'pending' : item.pending,
				'todoform' : todoform,
				}
	if todoform.is_valid():
		#print 'form is valid'
		item = todoform.save(commit = False)
		item.save()
		#print 'save the item'
		list = Todomodel.objects.all().order_by('-date')	
		return render(request,'Todoapp/list.html',{'list':list})
	return render(request,'Todoapp/register.html',context)
