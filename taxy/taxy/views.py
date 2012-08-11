from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, Template

def root(request):
    frontPageTemplate = get_template("frontpage.html")
    html = frontPageTemplate.render(Context( {} ))
    return HttpResponse(html)
