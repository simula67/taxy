from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, Template
from taxy.models import *
import datetime
from googlemaps import GoogleMaps,GoogleMapsError
from math import pi,cos

degree_to_radian = pi/180.0
radian_to_degree = 180.0/pi
def nearest_add(x,y):
    return "The Address"

"""
del_latlng: returns a pair which is the amount of change in latitude and longitude for given amount of thresholdRadius
This code is just gives a rough estimate assuming that 
* Earth is spherical
* Distance measured in miles
PS: del_lat is towards NORTH
and
del_lng is towards WEST
"""
def del_latlng(flat,flng,thresholdRadius=3.10686):
    earth_radius = 3963.1676
    del_lat = (thresholdRadius/earth_radius)*radians_to_degrees
    
    #Radius of circle at a given latitude
    tR = earth_radius*cos(flat*degree_to_radian)
    del_lng = (thresholdRadius/tR)*radian_to_degree
    
    return ( del_lat,del_lng)
"""
Returns the distance between 2 points from the GoogleAPI
"""

def dist_calc(from_add,to_add):
    my_map = GoogleMaps("")
    direct = my_map.directions(from_add,to_add)
    dist_meter = direct['Directions']['Distance']['meters']
    return dist_meter

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
class ConfirmationPost:
    def __init__(self):
        self.status = ""
        self.custPh = ""

def root(request):
    frontPageTemplate = get_template("frontpage.html")
    html = frontPageTemplate.render(Context( {} ))
    return HttpResponse(html)
def location_post(request):
    cabPh = request.GET['cabPh']
    lat = request.GET['x']
    lon = request.GET['y']
    theCab = Cab.objects.get(cabPhone=int(cabPh))
    theCab.lastX = lat
    theCab.lastY = lon
    theCab.lastUpdated = datetime.datetime.now()
    theCab.save()
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

def confirm_post(request):
    cabPh = request.GET['cabPh']
    trid = request.GET['trid']
    status = request.GET['status']
    pfare = float(request.GET['pfare'])
    theCab = Cab.objects.get(cabPhone=int(cabPh))
    theTrip = Trip.objects.get(tripId=int(trid))
    reject = 2
    if status == "OK":
        if theTrip.state == 1:
            reject = 0
            theTrip.state = 100
            theTrip.acceptedCab = theCab
            theTrip.save()
    if theTrip.state == 100:
        reject = 1
    if status == "NEG":
        if theTrip.proposedFare == pfare:
            if theTrip.state == 2:
                reject = 0
                theTrip.state = 100
                theTrip.acceptedCab = theCab
                theTrip.save()
            else:
                reject = 1
        else:
            reject = 1
            if theTrip.proposedFare < pfare:
                theTrip.prposedFare = pfare
                theTrip.fare = pfare #Hack
                thetrip.proposedCab = theCab
                theTrip.save()
    if theTrip.acceptedCab == theCab:
            reject = 0
    confirmationPost = ConfirmationPost()
    if reject == 0:
        confirmationPost.status = "OK"
        confimatioinPost.custPh = "%d" % theTrip.custPhone
    else:
        confirmationPost.status = "CANCEL"

    confirmationPostTemplate = get_template("confirmation_post.html")
    html = confirmationPostTemplate.render(Context( {'confirmationPost' : confirmationPost} ))
    return HttpResponse(html)

#TODO:
#Process get request from the index page. Returns trid, distance, approxCost
def trip_post(request):
    #Request contains fromX, fromY, toX, toY.
    #Add model to database
    theTrip = Trip()
    theTrip.fromX = request.GET['fromX']
    theTrip.fromY = request.GET['fromY']
    theTrip.toX = request.GET['toX']
    theTrip.toY = request.GET['toY']
    from_add = nearest_add(theTrip.fromX,theTrip.fromY)
    to_add = nearest_add(theTrip.toX,theTrip.toY)
    theTrip.dist = dist_calc(from_add,to_add)
    theTrip.tfDist = 1
    theTrip.fare = (theTrip.dist / 1000) * 10
    theTrip.state = 1
    theTrip.insertTrip = datetime.datetime.now()
    theTrip.proposedFare = 0
    theTrip.custPhone = int(request.GET['phone'])
    theTrip.save()
    
    #Do something with locationPost;
    #get trid
    tripSubmitTemplate = get_template("trip_submit.html")
    html = tripSubmitTemplate.render(Context( {'theTrip' : theTrip} ))
    return HttpResponse(html)

#TODO:
#Once the customer confirms, send the customer's phone number to the cabbie
def customer_confirm(request):
    #TODO:
    #check for get variable "accept". It's a radio button. If true then send details(from session) to cabbie's number
    #end session
    trip = Trip.objects.get(tripId=request.GET['tripId'])
    if request.GET['accept'] == "yes":
        trip.acceptedCab = request.GET['cabNo']
        trip.custPhone = int(request.GET['custPh'])
        trip.state = 100
        trip.save()
        return HttpResponse("Thank you for booking with Taxy. You will get a call from the cab driver soon.")
    else:
        trip.state = 2
        trip.save()
        return HttpResponse("We're sorry you couldn't find a cab :( . <a href="/">Try again?</a>");


