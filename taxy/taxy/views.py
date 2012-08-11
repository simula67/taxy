from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, Template
from taxy.models import *
def root(request):
    allCabs = Cab.objects.all()
    allTrips = Trip.objects.all()
    frontPageTemplate = get_template("frontpage.html")
    html = frontPageTemplate.render(Context( {} ))
    return HttpResponse(html)

