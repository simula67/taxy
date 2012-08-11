from django.db import models

class Trip(models.Model):
    tripId = models.AutoField(primary_key=True)
    fromX = models.DecimalField(max_digits=5, decimal_places=20)
    fromY = models.DecimalField(max_digits=5, decimal_places=20)
    toX = models.DecimalField(max_digits=5, decimal_places=20)
    toY = models.DecimalField(max_digits=5, decimal_places=20)
    dist = models.IntegerField(max_length=30)
    tfDist = models.IntegerField(max_length=30)
    fare =  models.DecimalField(max_digits=5, decimal_places=2)
    state =  models.IntegerField(max_length=30)
    insertTime = models.DateTimeField(auto_now=True)
    proposedFare =  models.DecimalField(max_digits=5, decimal_places=2)
    proposedCabs = models.ForeignKey('Cab')
    acceptedCab = models.ForeignKey('Cab')
    custPhone = models.IntegerField(max_length=20)



class Cab(models.Model):
    cabId = models.AutoField(primary_key=True)
    lastX = models.DecimalField(max_digits=5, decimal_places=20)
    lastY = models.DecimalField(max_digits=5, decimal_places=20)
    lastUpdated = models.DateTimeField()
    tripsEligible = models.ManyToManyField(Trip)
    def __unicode__(self):
        return self.name
