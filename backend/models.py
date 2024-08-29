from django.db import models

# Create your models here.
class THPT(models.Model):
    name = models.CharField(max_length=500)
    diachi = models.CharField(max_length=500)
    quan = models.CharField(max_length=500)
    ghichu = models.CharField(max_length=500, blank=True)
    nv1 = models.FloatField(blank=True, default=0)
    nv2 = models.FloatField(blank=True, default=0)
    nv3 = models.FloatField(blank=True, default=0)
    isChuyen = models.BooleanField(default=False)
    anh = models.ImageField(upload_to='thpt/',null=True,blank=True)
    monchuyen = models.CharField(max_length=500, blank=True)
    class Meta:
        ordering = ['-nv1', '-nv2', '-nv3'] 
    def __str__(self):
        return self.name + " | " + self.monchuyen
    def getaddress(self):
        return self.diachi
    
class District(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name


class VisitorCount(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'Visitor Count: {self.count}'