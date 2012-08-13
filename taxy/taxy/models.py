from django.db import models

class Trip(models.Model):
    tripId = models.AutoField(primary_key=True)
    fromX = models.DecimalField(max_digits=20, decimal_places=10)
    fromY = models.DecimalField(max_digits=20, decimal_places=10)
    toX = models.DecimalField(max_digits=20, decimal_places=10)
    toY = models.DecimalField(max_digits=20, decimal_places=10)
    dist = models.IntegerField(max_length=30)
    tfDist = models.IntegerField(max_length=30,null=True, blank=True)
    fare =  models.DecimalField(max_digits=5, decimal_places=2)
    state =  models.IntegerField(max_length=30) # 0 test, 1 open ,2 acccepted neg, 100 done and dusted,
    insertTime = models.DateTimeField(auto_now=True)
    proposedFare =  models.DecimalField(max_digits=10, decimal_places=2)
    proposedCab = models.ForeignKey('Cab',related_name="proposed",null=True, blank=True,default=None)
    acceptedCab = models.ForeignKey('Cab',related_name="accepted",null=True, blank=True,default=None)
    custPhone = models.IntegerField(max_length=20)
    def __unicode__(self):
        return u'%d' % self.tripId


class Cab(models.Model):
    cabNo = models.CharField(max_length=50)
    cabPhone = models.IntegerField(max_length=20)
    lastX = models.DecimalField(max_digits=20, decimal_places=10)
    lastY = models.DecimalField(max_digits=20, decimal_places=10)
    lastUpdated = models.DateTimeField()
    tripsEligible = models.ManyToManyField(Trip,null=True)
    def __unicode__(self):
        return u'%d' % self.cabPhone
