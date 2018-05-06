from __future__ import unicode_literals

from django.db import models
from datetime import date
#from django.utils import timezone
# Create your models here.
class Todomodel(models.Model):
	CHOICES_STATUS = (('1', 'Pending',), ('2', 'Done',),('3','Not Required'))
	employee_num = models.IntegerField(default=1)
	date = models.DateField(default = date.today()) #date.today()
	description = models.TextField(max_length = 500,blank=False)
	status = models.CharField(choices=CHOICES_STATUS,max_length=10,default='Pending')

	def __str__(self):
		return str(self.date)+ " " +str(self.description) #+" "+str(self.pending)+" "+str(self.done)
