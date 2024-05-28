from django.db import models

class Anchor(models.Model):
    anchorID = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.anchorID

class TagDistance(models.Model):
    anchor = models.ForeignKey(Anchor, related_name='tag_distances', on_delete=models.CASCADE)
    deviceID = models.CharField(max_length=20)
    TimeStampUTC = models.DateTimeField(auto_now_add=True)
    distance = models.IntegerField()

    def __str__(self):
        return f'{self.deviceID} - {self.distance}m'
