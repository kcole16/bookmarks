from django.db import models
from django.contrib.auth.models import User

class List(models.Model):
    name = models.CharField(max_length = 50)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    #links = models.ManyToManyField('Link', blank = True)


class Link(models.Model):
	lists = models.ForeignKey(List)
	name = models.CharField(max_length = 50)
	link = models.URLField()
	date_created = models.DateTimeField(auto_now_add = True)
	date_modified = models.DateTimeField(auto_now = True)
	tags = models.TextField(null = True, blank = True)

class User(models.Model):
	user = models.OneToOneField(User)
	internal_id = models.CharField(max_length = 25, null = True, blank= True)
	verified = models.BooleanField(default = False)
	approval_date = models.DateTimeField(null = True, blank = True)

	



