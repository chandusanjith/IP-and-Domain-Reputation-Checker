from django.db import models
from django.conf import settings


class ips(models.Model):
  reference = models.TextField(default = 1)
  ipaddress  = models.TextField()
  status = models.TextField()
  remarks = models.TextField(default="")
  Sans = models.TextField(default="")
  Pysbil = models.TextField(default="")
  VirusTotal = models.TextField(default="")
  IbmXForce = models.TextField(default="")
   
  def __str__(self):
       return "{}-{}".format(self.ipaddress, self.reference)

class contacted(models.Model):
	name = models.TextField()
	email = models.TextField()
	message = models.TextField()
	mobile = models.TextField()
	dateofcontact = models.TextField()

  
  

class IPData(models.Model):
  ipcount = models.IntegerField()
  blacklistedip = models.IntegerField()
  goodip = models.IntegerField()
  domaincount = models.IntegerField()
  hashcount = models.IntegerField(default=1)

  def __str__(self):
       return "{}-{}".format(self.ipcount, self.blacklistedip)

class CountryData(models.Model):
  country = models.TextField()
  blklistcount = models.IntegerField()

  def __str__(self):
       return "{}-{}".format(self.country, self.blklistcount)

class Hashes(models.Model):
  reference = models.TextField(null=True)
  hashes = models.TextField(null=True)
  family = models.TextField(null=True)
  type = models.TextField(null=True)
  risk = models.TextField(null=True)