from django.db import models

class ips(models.Model):
  reference = models.TextField(default = 1)
  ipaddress  = models.TextField()
  status = models.TextField()
  remarks = models.TextField(default="")


class contacted(models.Model):
	name = models.TextField()
	email = models.TextField()
	message = models.TextField()
	mobile = models.TextField()
	dateofcontact = models.TextField()