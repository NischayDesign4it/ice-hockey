from django.db import models

class Transmitter(models.Model):
    transmitterSerialNumber = models.CharField(max_length=20)
    nodeType = models.CharField(max_length=20)
    nodeSerialNumber = models.CharField(max_length=20, null=True, blank=True)
    allCount = models.IntegerField(null=True, blank=True)

class Read(models.Model):
    transmitter = models.ForeignKey(Transmitter, related_name='reads', on_delete=models.CASCADE)
    timeStampUTC = models.DateTimeField(auto_now_add=True)
    lastTimeStamp = models.DateTimeField(null=True)
    deviceUID = models.CharField(max_length=20)
    manufacturerName = models.CharField(max_length=100)
    distance1 = models.IntegerField(null=True, blank=True)
    distance2 = models.IntegerField(null=True, blank=True)
    distance3 = models.IntegerField(null=True, blank=True)
    distance4 = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, default='Out')



class StatusLog(models.Model):
    deviceUID = models.CharField(max_length=255)
    status = models.CharField(max_length=10)  # Assuming status is 'In' or 'Out'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.deviceUID} - {self.status} at {self.timestamp}"



