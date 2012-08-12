from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, Template
from taxy.models import *
import datetime
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
    locationPost = LocationPost();
    #Do something with locationPost;
    #get trid
    tripSubmitTemplate = get_template("trip_submit.html")
    html = tripSubmitTemplate.render(Context( {'cabPh': cabPh, 'cabNo': cabNo, 'locationPost': locationPost, 'custPhone': request.POST['phone']} ))

    return HttpResponse(html)

#TODO:
#Once the customer confirms, send the customer's phone number to the cabbie
def customer_confirm(request):
    pass
    #TODO:
    #check for get variable "accept". It's a radio button. If true then send details(from session) to cabbie's number
    #end session

