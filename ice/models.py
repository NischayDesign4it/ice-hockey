from django.db import models


class Transmitter(models.Model):
    transmitterSerialNumber = models.CharField(max_length=20)
    nodeType = models.CharField(max_length=20)
    allCount = models.IntegerField()

class Read(models.Model):
    transmitter = models.ForeignKey(Transmitter, related_name='reads', on_delete=models.CASCADE)
    timeStampUTC = models.CharField(max_length=20)
    deviceUID = models.CharField(max_length=20)
    manufacturerName = models.CharField(max_length=100)
    distance = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)



from django.shortcuts import render
from .models import Transmitter

def transmitter_list(request):
    transmitters = Transmitter.objects.all()
    return render(request, 'your_app/transmitter_list.html', {'transmitters': transmitters})
