from django.db import models

class Anchor(models.Model):
    anchorID = models.CharField(max_length=50)

    def __str__(self):
        return self.anchorID

class TagDistance(models.Model):
    anchor = models.ForeignKey(Anchor, related_name='tag_distances', on_delete=models.CASCADE)
    deviceID = models.CharField(max_length=20)
    TimeStampUTC = models.DateTimeField(auto_now_add=True)
    distance = models.IntegerField()

    def __str__(self):
        return f'{self.deviceID} - {self.distance}m'



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
    distance = models.IntegerField()
    count = models.IntegerField()
