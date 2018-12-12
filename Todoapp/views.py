from django.shortcuts import render,redirect,reverse
from . models import Todomodel
import datetime
from datetime import date
from .forms import Todoform
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def register(request):
	if request.method == 'POST': # for a form with data in it
		todoform = Todoform(request.POST)
		if todoform.is_valid():
			item = todoform.save(commit = False)
			item.employee_num = request.user
			item.save()
			messages.success(request, 'Item saved')
	# request.session.set_expiry(300)
	# get_expire_at_browser_close			
	todoform = Todoform() #just for displaying empty form
	list = Todomodel.objects.filter(date=datetime.date.today(),employee_num = request.user)
	pending_list = Todomodel.objects.filter(status='1',employee_num = request.user).order_by('-date')
	return render (request,'Todoapp/register.html',{'todoform':todoform,'list':list,'pending_list':pending_list})
		
def list(request):
	list = Todomodel.objects.filter(employee_num = request.user).order_by('-date')	
	return render(request,'Todoapp/list.html',{'list':list})

def details(request,item_id):
	item = get_object_or_404(Todomodel,id=item_id)
	return render(request,'Todoapp/details.html',{'item':item})

def edit(request,item_id=None):	
	item = Todomodel.objects.get(pk = item_id)
	todoform = Todoform(request.POST or None,instance = item)
	context = { 'date' : item.date,
				'description' : item.description,
				'todoform' : todoform,
				}
	if todoform.is_valid():
		if request.POST.get('status',None)=='4':
			item = get_object_or_404(Todomodel,pk = item_id)
			print ('deleting--->{}',format(item))
			item.delete()
			messages.success(request, 'Item deleted')
			todoform = Todoform() #just for displaying empty form
			list = Todomodel.objects.filter(date=datetime.date.today(),employee_num = request.user)
			pending_list = Todomodel.objects.filter(status='1',employee_num = request.user)
			print('before render')
			context = {
						'todoform':todoform,'list':list,
						'pending_list':pending_list,
						'msg' : 'Deleted successfully!!!'
						}
			return redirect('todoapp:register')

		item = todoform.save(commit = False)
		item.save()
		messages.success(request, 'Item modified')
		print('should not come here')
		list = Todomodel.objects.filter(date=datetime.date.today(),employee_num = request.user)
		pending_list = Todomodel.objects.filter(status='1',employee_num = request.user).order_by('-date')
		return render (request,'Todoapp/register.html',{'todoform':Todoform(),'list':list,'pending_list':pending_list})
	return render(request,'Todoapp/register.html',context)
