# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Location
# Create your views here.


def index(request):
    location_list = Location.objects.all()
    template = loader.get_template('plotdata/index.html')
    context = {
        'location_list': location_list,
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("hello World. You are at the plotdata index")


def detail(request, location_id):
    return HttpResponse("You're looking at location %s." % location_id)
