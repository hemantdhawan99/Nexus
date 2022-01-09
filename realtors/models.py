from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator

class Realtor(models.Model):
	phoneNumberRegex = RegexValidator(regex = r"^\+?\d[\d -]{8,12}\d$")
	name = models.CharField(max_length=200)
	photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
	description = models.TextField(blank=True)
	phone = models.CharField(validators = [phoneNumberRegex], max_length = 12, null= True)
	email = models.CharField(max_length=200)
	is_mvp = models.BooleanField(default=False)
	hire_date = models.DateTimeField(default=datetime.now,blank=True)
	def __str__(self):
		return self.name