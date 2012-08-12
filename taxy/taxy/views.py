from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, Template
from taxy.models import *
class LocationPost:
    def __init__(self):   
        self.tripId = ""
        self.fromX = ""
        self.fromY = ""
        self.toX = ""
        self.toY = ""
        self.distance = ""
        self.fare = ""
        self.tfDist = ""
def root(request):
    frontPageTemplate = get_template("frontpage.html")
    html = frontPageTemplate.render(Context( {} ))
    return HttpResponse(html)
def location_post(request):
    cabPh = request.GET['cabPh']
    lat = request.GET['x']
    lon = request.GET['y']
    theCab = Cab.objects.get(cabPhone=int(cabPh))
    
    locationPosts = []
    for i in theCab.tripsEligible.all():
        locationPost = LocationPost()
        locationPost.tripId = i.tripId
        locationPost.fromX = i.fromX
        locationPost.fromY = i.fromY
        locationPost.toX = i.toX
        locationPost.toY = i.toY
        locationPost.distance = i.dist
        locationPost.fare = i.fare
        locationPost.tfDist = i.tfDist
        locationPosts.append(locationPost)
    locationPostTemplate = get_template("location_post.html")
    html = locationPostTemplate.render(Context( {'locationPosts' : locationPosts} ))
    return HttpResponse(html)

