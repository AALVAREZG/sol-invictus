# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse
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
    location = get_object_or_404(Location, pk=location_id)
    return render(request, 'plotdata/detail.html', {'location': location})

    # return HttpResponse("You're looking at location %s." % location_id)


def edit(request, location_id):
    print("EDIT VIEW ***********************")
    location = get_object_or_404(Location, pk=location_id)
    return render(request, 'plotdata/edit.html', {'location': location})


def save(request, location_id):
    print("save VIEW &&&&&&&&&&&&&&&&&&&&&&&&&")
    try:
        location = get_object_or_404(Location, pk=location_id)
        location.loc_description_text = request.POST['description']
        print("location from post object", location)
    except (KeyError, Location.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'plotdata/detail.html', {
            'location': location,
            'error_message': "You didn't select a location.",
        })
    else:
        location.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('plotdata:detail',
                                    args=(location_id,)))
